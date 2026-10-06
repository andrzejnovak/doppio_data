"""Merge per-file skims into per-process ROOT files with event weights.

data: golden-JSON mask; integrated luminosity = sum of recorded lumi (pp_2016lumibyls.csv) over the
      (run, LS) pairs seen in the processed files AND in the golden JSON.
MC:   weight = xsec[pb] * L[pb^-1] * genWeight / sum(genEventSumw over processed files)
"""

import csv
import glob
import json
import os

import numpy as np
import uproot

ROOT = os.path.dirname(os.path.abspath(__file__))
BR_HAD = 0.6741
SIGMA_TT = 831.76  # pb, NNLO+NNLL (Top++ v2.0), mt = 172.5 GeV; +19.77 -29.20 (scale) +35.06 (PDF+as)
# (cross section [pb], relative uncertainty, source)
XSEC = {
    "TTToHadronic_TuneCP5_13TeV-powheg-pythia8": (SIGMA_TT * BR_HAD**2, 0.06, "NNLO+NNLL sigma_tt x BR(had)^2"),
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8": (SIGMA_TT * 2 * BR_HAD * (1 - BR_HAD), 0.06,
                                                      "NNLO+NNLL sigma_tt x 2 BR(had) BR(lep)"),
    # W/Z: LO MadGraph, approximate (the W/Z rate is the fitted signal strength; for validation only)
    "WJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8": (315.2, 0.2, "approx. LO MG (XSDB-like)"),
    "WJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8": (68.58, 0.2, "approx. LO MG (XSDB-like)"),
    "WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8": (34.69, 0.2, "approx. LO MG (XSDB-like)"),
    "ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8": (145.3, 0.2, "approx. LO MG (XSDB-like)"),
    "ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8": (34.29, 0.2, "approx. LO MG (XSDB-like)"),
    "ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8": (18.57, 0.2, "approx. LO MG (XSDB-like)"),
    # QCD: LO MadGraph; QCD normalisation floats in rhalphabet (validation only)
    "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8": (32100.0, 0.3, "LO MG"),
    "QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8": (6831.0, 0.3, "LO MG"),
    "QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8": (1207.0, 0.3, "LO MG"),
    "QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8": (119.9, 0.3, "LO MG"),
    "QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8": (25.24, 0.3, "LO MG"),
}
GROUPS = {"JetHT": ["JetHT_Run2016G", "JetHT_Run2016H"], "TT": [k for k in XSEC if k.startswith("TT")],
          "WQQ": [k for k in XSEC if k.startswith("WJets")], "ZQQ": [k for k in XSEC if k.startswith("ZJets")],
          "QCD": [k for k in XSEC if k.startswith("QCD")]}


def load(sample):
    files = sorted(glob.glob(f"{ROOT}/skims/{sample}/*.npz"))
    data = [np.load(f) for f in files]
    data = [d for d in data if "run" in d.files]
    cols = [k for k in data[0].files if not k.startswith("meta_")]
    out = {k: np.concatenate([d[k] for d in data]) for k in cols}
    meta = {"n_files": len(files), "n_events_read": int(sum(int(np.load(f)["meta_n_events_file"]) for f in files)),
            "lumisections": np.concatenate([np.load(f)["meta_lumisections"] for f in files])}
    if "meta_genEventSumw" in np.load(files[0]).files:
        meta["sumw"] = float(sum(float(np.load(f)["meta_genEventSumw"]) for f in files))
    return out, meta


def golden():
    js = json.load(open(f"{ROOT}/meta/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"))
    good = set()
    for run, ranges in js.items():
        for a, b in ranges:
            good.update((int(run), ls) for ls in range(a, b + 1))
    return good


def lumi_table():
    lumi = {}
    with open(f"{ROOT}/meta/pp_2016lumibyls.csv") as f:
        for row in csv.reader(l for l in f if not l.startswith("#")):
            run = int(row[0].split(":")[0]); ls = int(row[1].split(":")[0])
            lumi[(run, ls)] = float(row[6])  # recorded, /fb
    return lumi


def write(name, arrays):
    path = f"{ROOT}/output/{name}.root"
    with uproot.recreate(path) as f:
        f["Events"] = arrays
    return path


def main():
    os.makedirs(f"{ROOT}/output", exist_ok=True)
    good, lumi = golden(), lumi_table()
    summary = {}
    # data
    parts, seen = [], set()
    for s in GROUPS["JetHT"]:
        d, m = load(s)
        mask = np.array([(r, l) in good for r, l in zip(d["run"].tolist(), d["lumi"].tolist())])
        parts.append({k: v[mask] for k, v in d.items()})
        seen.update(map(tuple, m["lumisections"].tolist()))
        summary[s] = dict(n_files=m["n_files"], n_events_read=m["n_events_read"], n_selected=int(mask.sum()))
    used = seen & good
    L = sum(lumi.get(x, 0.0) for x in used)
    missing = len([x for x in used if x not in lumi])
    data = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}
    write("JetHT", data)
    summary["luminosity_fb"] = L
    summary["lumisections_used"] = len(used)
    summary["lumisections_missing_in_csv"] = missing
    # MC
    for group in ("TT", "WQQ", "ZQQ", "QCD"):
        parts = []
        for s in GROUPS[group]:
            if not glob.glob(f"{ROOT}/skims/{s}/*.npz"):
                continue
            d, m = load(s)
            xs, unc, src = XSEC[s]
            d["weight"] = (xs * L * 1000.0 * d["genWeight"] / m["sumw"]).astype(np.float32)
            d["sample_id"] = np.full(len(d["run"]), list(XSEC).index(s), np.int16)
            parts.append(d)
            summary[s] = dict(n_files=m["n_files"], n_events_read=m["n_events_read"], sumw=m["sumw"],
                              n_selected=len(d["run"]), xsec_pb=xs, xsec_rel_unc=unc, xsec_source=src,
                              expected_events=float(d["weight"].sum()))
        if parts:
            keys = set.intersection(*[set(p) for p in parts])
            write(group, {k: np.concatenate([p[k] for p in parts]) for k in sorted(keys)})
    json.dump(summary, open(f"{ROOT}/output/summary.json", "w"), indent=2)
    print(json.dumps({k: v for k, v in summary.items() if not isinstance(v, dict)}, indent=1))


if __name__ == "__main__":
    main()
