#!/usr/bin/env python
"""Skim CMS BACON ROOT files for the Wqq dataset, splitting outputs to fit git's 100 MB per-file limit.

Reads source files from --src-dir, applies cuts (vjet0_pt > 300, vjet0_msd0 > 20),
keeps only the branches the doppio Wqq loader uses, and writes ZSTD(22) ROOT outputs
split into N parts each.

Usage:
    pixi run python make_wqq_skim.py --src-dir data/data --out-dir Wqq
"""
from __future__ import annotations

import argparse
import hashlib
import os
import time
from pathlib import Path

import uproot

WQQ_BASE_FEATURES = [
    "vjet0_csv",
    "vjet0_t1", "vjet0_t2", "vjet0_t3",
    "vjet0_pullAngle",
    "vjet0_sj1_csv", "vjet0_sj2_csv",
    "vjet0_sj1_q", "vjet0_sj2_q",
    "vjet0_sj1_z", "vjet0_sj2_z",
    "vjet0_c2b0", "vjet0_c2b0P2", "vjet0_c2b0P5", "vjet0_c2b1P0", "vjet0_c2b2P0",
    "vjet0_qjet",
]
KEEP = WQQ_BASE_FEATURES + ["vjet0_msd0", "vjet0_pt", "trigger"]

# (source filename, output basename, n_splits)
JOBS = [
    ("TT.root",      "TT_skim",      1),
    ("QCD_s.root",   "QCD_skim",     3),
    ("JetHT_s.root", "JetHT_skim",   5),
]


def md5sum(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def skim_one(src: Path, out_dir: Path, basename: str, n_splits: int, compression):
    f = uproot.open(src)
    tree = f[next(iter(f.keys())).split(";")[0]]
    arrays = tree.arrays(KEEP, library="np")
    mask = (arrays["vjet0_pt"] > 300) & (arrays["vjet0_msd0"] > 20)
    n_kept = int(mask.sum())
    out_arrs = {k: v[mask] for k, v in arrays.items()}

    if n_splits == 1:
        chunks = [(0, 0, n_kept)]
    else:
        size = n_kept // n_splits
        chunks = [(i, i * size, (i + 1) * size if i < n_splits - 1 else n_kept) for i in range(n_splits)]

    results = []
    for i, lo, hi in chunks:
        out = out_dir / (f"{basename}.root" if n_splits == 1 else f"{basename}_part{i}.root")
        if out.exists():
            out.unlink()
        chunk_arrs = {k: v[lo:hi] for k, v in out_arrs.items()}
        t0 = time.time()
        with uproot.recreate(out, compression=compression) as fo:
            fo["Tree"] = chunk_arrs
        dt = time.time() - t0
        sz = out.stat().st_size
        md5 = md5sum(out)
        results.append((out.name, hi - lo, sz, md5, dt))
        print(f"  {out.name:<32} events={hi - lo:>10,}  size={sz / 1e6:>7.2f} MB  md5={md5}  ({dt:.1f}s)")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-dir", required=True, type=Path, help="Directory with source ROOT files")
    ap.add_argument("--out-dir", required=True, type=Path, help="Output directory for skimmed files")
    ap.add_argument("--compression", default="zstd22", choices=["zstd22", "zstd9", "lzma9"])
    args = ap.parse_args()

    comp = {"zstd22": uproot.ZSTD(22), "zstd9": uproot.ZSTD(9), "lzma9": uproot.LZMA(9)}[args.compression]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Cuts:        vjet0_pt > 300  AND  vjet0_msd0 > 20")
    print(f"Branches:    {len(KEEP)} kept (drops ~108 of 128)")
    print(f"Compression: {args.compression}")
    print()

    all_results = []
    for src_name, basename, n_splits in JOBS:
        src = args.src_dir / src_name
        if not src.exists():
            print(f"!! Skipping {src} — not found")
            continue
        print(f"=== {src.name} -> {basename} (splits={n_splits}) ===")
        all_results.extend((src.name, *r) for r in skim_one(src, args.out_dir, basename, n_splits, comp))
        print()

    print("=== Summary ===")
    total = sum(r[3] for r in all_results)
    print(f"Total: {len(all_results)} files, {total / 1e6:.1f} MB")
    print()
    print("MD5 checksums (for DATASETS.md):")
    for src_name, name, _, sz, md5, _ in all_results:
        print(f"  {md5}  Wqq/{name}")


if __name__ == "__main__":
    main()
