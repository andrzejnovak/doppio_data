"""Skim one CMS Open Data UL2016 NanoAOD file into a Wqq-style flat table.

Selection (data and MC alike):
  trigger  HLT_PFJet450 | HLT_AK8PFJet450 | HLT_PFHT900   (unprescaled in 2016G/H; no trimmed-mass triggers)
  leading AK8 FatJet (index 0, pt-ordered) with tight jetId (bit 2), |eta| < 2.4, pt > PT_MIN, 30 < msoftdrop < 250

Usage: python skim.py <xrootd path> <output.npz> [--mc]
"""

import sys

import awkward as ak
import numpy as np
import uproot

PT_MIN = 525.0
TRIGGERS = ("HLT_PFJet450", "HLT_AK8PFJet450", "HLT_PFHT900")
FJ = ["pt", "eta", "phi", "msoftdrop", "mass", "tau1", "tau2", "tau3", "tau4", "n2b1", "n3b1", "btagDeepB",
      "nConstituents", "lsf3", "jetId", "subJetIdx1", "subJetIdx2",
      # taggers: stored but flagged; non-MD ParticleNet/DeepAK8 are strongly mass-correlated
      "deepTag_WvsQCD", "deepTagMD_WvsQCD", "particleNet_WvsQCD", "particleNetMD_Xqq", "particleNetMD_Xcc",
      "particleNetMD_Xbb", "particleNetMD_QCD"]
FJ_MC = ["hadronFlavour", "nBHadrons", "nCHadrons"]
SJ = ["pt", "eta", "phi", "mass", "btagDeepB"]
GEN = ["pt", "eta", "phi", "pdgId", "status", "statusFlags", "genPartIdxMother"]


def dphi(a, b):
    return (a - b + np.pi) % (2 * np.pi) - np.pi


def gen_match(ev, fj_eta, fj_phi):
    """Per selected event: nearest last-copy W/Z to the jet and containment of its quark daughters."""
    n = len(fj_eta)
    out = {k: np.zeros(n, dtype=np.float32) for k in ("gen_V_pt", "gen_V_dR", "gen_qq_dRmax", "gen_b_dR")}
    out.update({k: np.zeros(n, dtype=np.int8) for k in ("gen_V_pdg", "gen_V_from_top")})
    out["gen_V_dR"][:] = 99; out["gen_qq_dRmax"][:] = 99; out["gen_b_dR"][:] = 99
    counts = ak.to_numpy(ak.num(ev["GenPart_pdgId"]))
    offs = np.concatenate([[0], np.cumsum(counts)])
    flat = {b: ak.to_numpy(ak.flatten(ev[f"GenPart_{b}"])) for b in ("pdgId", "statusFlags", "genPartIdxMother",
                                                                      "eta", "phi", "pt")}
    for i in range(n):
        sl = slice(offs[i], offs[i + 1])
        p, f, m = flat["pdgId"][sl], flat["statusFlags"][sl], flat["genPartIdxMother"][sl]
        e, ph, ptt = flat["eta"][sl], flat["phi"][sl], flat["pt"][sl]
        last = (f >> 13) & 1 == 1
        cand = np.where(last & ((np.abs(p) == 24) | (np.abs(p) == 23)))[0]
        if len(cand) == 0:
            continue
        dr = np.hypot(e[cand] - fj_eta[i], dphi(ph[cand], fj_phi[i]))
        j = cand[np.argmin(dr)]
        out["gen_V_pdg"][i] = abs(p[j]); out["gen_V_pt"][i] = ptt[j]; out["gen_V_dR"][i] = dr.min()
        dau = np.where((m == j) & (np.abs(p) < 6))[0]
        if len(dau) >= 2:
            out["gen_qq_dRmax"][i] = np.hypot(e[dau] - fj_eta[i], dphi(ph[dau], fj_phi[i])).max()
        # walk up the mother chain: is this W from a top?
        k = j
        for _ in range(50):
            k = m[k]
            if k < 0:
                break
            if abs(p[k]) == 6:
                out["gen_V_from_top"][i] = 1
                bs = np.where((m == k) & (np.abs(p) == 5))[0]
                if len(bs):
                    out["gen_b_dR"][i] = np.hypot(e[bs] - fj_eta[i], dphi(ph[bs], fj_phi[i])).min()
                break
    return out


def main(path, output, mc):
    f = uproot.open(path, timeout=600)
    tree = f["Events"]
    keys = set(tree.keys())
    trig = [t for t in TRIGGERS if t in keys]
    fj = FJ + (FJ_MC if mc else [])
    branches = ["run", "luminosityBlock", "event", "nFatJet", "PV_npvsGood"] + trig + [f"FatJet_{b}" for b in fj]
    branches += [f"SubJet_{b}" for b in SJ]
    if mc:
        branches += ["genWeight", "Pileup_nTrueInt", "LHE_HT"] + [f"GenPart_{b}" for b in GEN]
    branches = [b for b in branches if b in keys]
    rows, lumis = [], set()
    for ev in tree.iterate(branches, step_size="200 MB"):
        lumis.update(zip(ak.to_numpy(ev["run"]).tolist(), ak.to_numpy(ev["luminosityBlock"]).tolist()))
        fired = np.zeros(len(ev), bool)
        for t in trig:
            fired |= ak.to_numpy(ev[t])
        has = ak.to_numpy(ev["nFatJet"]) > 0
        lead = ak.firsts(ev["FatJet_pt"])
        sel = fired & has
        pt0 = ak.to_numpy(ak.fill_none(lead, 0.0))
        eta0 = ak.to_numpy(ak.fill_none(ak.firsts(ev["FatJet_eta"]), 9.0))
        msd0 = ak.to_numpy(ak.fill_none(ak.firsts(ev["FatJet_msoftdrop"]), 0.0))
        jid0 = ak.to_numpy(ak.fill_none(ak.firsts(ev["FatJet_jetId"]), 0))
        sel &= (pt0 > PT_MIN) & (np.abs(eta0) < 2.4) & ((jid0 & 2) > 0) & (msd0 > 30) & (msd0 < 250)
        s = ev[sel]
        if len(s) == 0:
            continue
        r = {"run": ak.to_numpy(s["run"]).astype(np.int32), "lumi": ak.to_numpy(s["luminosityBlock"]).astype(np.int32),
             "event": ak.to_numpy(s["event"]).astype(np.uint64), "npv": ak.to_numpy(s["PV_npvsGood"]).astype(np.int16)}
        for t in trig:
            r[t] = ak.to_numpy(s[t]).astype(np.int8)
        for b in fj:
            r[f"fj_{b}"] = ak.to_numpy(ak.firsts(s[f"FatJet_{b}"])).astype(np.float32)
        # subjets of the leading fat jet
        for which in (1, 2):
            idx = ak.to_numpy(ak.firsts(s[f"FatJet_subJetIdx{which}"])).astype(int)
            for b in SJ:
                arr = s[f"SubJet_{b}"]
                vals = np.full(len(s), -1.0, np.float32)
                ok = idx >= 0
                if ok.any():
                    counts = ak.to_numpy(ak.num(arr))
                    ok &= idx < counts
                    flat = ak.to_numpy(ak.flatten(arr))
                    offs = np.concatenate([[0], np.cumsum(counts)[:-1]])
                    vals[ok] = flat[offs[ok] + idx[ok]]
                r[f"sj{which}_{b}"] = vals
        if mc:
            r["genWeight"] = ak.to_numpy(s["genWeight"]).astype(np.float32)
            for b in ("Pileup_nTrueInt", "LHE_HT"):
                if b in s.fields:
                    r[b] = ak.to_numpy(s[b]).astype(np.float32)
            r.update(gen_match(s, r["fj_eta"], r["fj_phi"]))
        rows.append(r)
    out = {k: np.concatenate([x[k] for x in rows]) for k in rows[0]} if rows else {}
    meta = {"source": np.array(path), "pt_min": np.array(PT_MIN), "triggers": np.array(",".join(trig)),
            "n_events_file": np.array(tree.num_entries)}
    lum = np.array(sorted(lumis), dtype=np.int64).reshape(-1, 2)
    meta["lumisections"] = lum
    if mc:
        runs = f["Runs"].arrays(["genEventSumw", "genEventCount"], library="np")
        meta["genEventSumw"] = np.array(runs["genEventSumw"].sum())
        meta["genEventCount"] = np.array(runs["genEventCount"].sum())
    np.savez_compressed(output, **out, **{f"meta_{k}": v for k, v in meta.items()})
    print(f"{path}: {tree.num_entries} -> {len(out.get('run', []))} selected")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--mc" in sys.argv)
