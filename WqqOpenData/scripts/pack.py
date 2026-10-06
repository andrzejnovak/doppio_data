"""Recompress merged Wqq open-data outputs and split them into <95 MB parts for git.

Usage: python pack.py <merged_output_dir> <dest_dir>

Each <Sample>.root becomes <Sample>_part<k>.root (k = 0, 1, ...), split sequentially
by entry, so concatenating the parts in k order reproduces the original raw-row order
(doppio folds and the QCD unweighting are keyed on that order). ZSTD level 22.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import uproot

SAMPLES = sys.argv[3].split(",") if len(sys.argv) > 3 else ["JetHT", "QCD", "TT", "WQQ", "ZQQ"]
TARGET_BYTES = 85e6


def write(path, arrays):
    with uproot.recreate(path, compression=uproot.ZSTD(22)) as f:
        f["Events"] = arrays


def main(src, dst):
    src, dst = Path(src), Path(dst)
    manifest = {}
    for s in SAMPLES:
        tree = uproot.open(src / f"{s}.root")["Events"]
        arrays = {k: tree[k].array(library="np") for k in tree.keys()}
        n = tree.num_entries
        probe = min(n, 200_000)
        tmp = dst / f".{s}_probe.root"
        write(tmp, {k: v[:probe] for k, v in arrays.items()})
        per_event = tmp.stat().st_size / probe
        tmp.unlink()
        step = int(TARGET_BYTES / per_event)
        parts = []
        for k, start in enumerate(range(0, n, step)):
            p = dst / f"{s}_part{k}.root"
            write(p, {key: v[start:start + step] for key, v in arrays.items()})
            size = p.stat().st_size
            if size > 95e6:
                raise RuntimeError(f"{p} is {size / 1e6:.1f} MB; lower TARGET_BYTES")
            parts.append({"file": p.name, "entries": int(min(step, n - start)), "bytes": size,
                          "md5": hashlib.md5(p.read_bytes()).hexdigest()})
            print(p.name, parts[-1]["entries"], f"{size / 1e6:.1f} MB", flush=True)
        manifest[s] = {"entries": int(n), "parts": parts}
    (dst / "parts.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:3])
