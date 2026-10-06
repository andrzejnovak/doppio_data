"""Data vs weighted MC validation of the open-data Wqq skim.

Plots soft-drop mass (40-200 GeV) inclusive and after two tagger cuts, stacked MC (QCD, tt, W, Z) vs data,
with MC at its absolute normalisation and with QCD scaled to match the data total (W/Z/tt fixed).
Quantifies the tt and W/Z fractions in the W window (65-100 GeV) of the pass region.
"""

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import uproot

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = f"{ROOT}/validation"
BINS = np.linspace(40, 200, 33)
COLORS = {"QCD": "#c3c2b7", "TT": "#eb6834", "WQQ": "#2a78d6", "ZQQ": "#1baf7a"}


def load(name):
    t = uproot.open(f"{ROOT}/output/{name}.root")["Events"]
    cols = ["fj_msoftdrop", "fj_pt", "fj_tau1", "fj_tau2", "fj_particleNetMD_Xqq", "fj_particleNetMD_QCD"]
    cols += ["weight"] if name != "JetHT" else []
    cols += ["gen_V_pdg", "gen_qq_dRmax", "gen_V_from_top", "gen_b_dR"] if name != "JetHT" else []
    d = {c: t[c].array(library="np") for c in cols}
    d["tau21"] = np.where(d["fj_tau1"] > 0, d["fj_tau2"] / np.maximum(d["fj_tau1"], 1e-9), 1.0)
    d["pnmd"] = d["fj_particleNetMD_Xqq"] / np.maximum(d["fj_particleNetMD_Xqq"] + d["fj_particleNetMD_QCD"], 1e-9)
    if "weight" not in d:
        d["weight"] = np.ones(len(d["fj_msoftdrop"]))
    return d


def main():
    os.makedirs(OUT, exist_ok=True)
    s = {n: load(n) for n in ("JetHT", "QCD", "TT", "WQQ", "ZQQ")}
    cuts = {"inclusive": lambda d: np.ones(len(d["tau21"]), bool),
            "tau21<0.35": lambda d: d["tau21"] < 0.35,
            "PNMD_Xqq>0.9": lambda d: d["pnmd"] > 0.9}
    report = {}
    for cname, cut in cuts.items():
        h = {n: np.histogram(d["fj_msoftdrop"][cut(d)], BINS, weights=d["weight"][cut(d)])[0] for n, d in s.items()}
        data = h.pop("JetHT")
        mc_tot = sum(h.values())
        kq = (data.sum() - h["TT"].sum() - h["WQQ"].sum() - h["ZQQ"].sum()) / max(h["QCD"].sum(), 1e-9)
        win = (BINS[:-1] >= 65) & (BINS[1:] <= 100)
        hs = dict(h, QCD=h["QCD"] * kq)
        tot_win = sum(v[win].sum() for v in hs.values())
        report[cname] = dict(data=float(data.sum()), mc_abs=float(mc_tot.sum()), data_over_mc_abs=float(data.sum() / mc_tot.sum()),
                             qcd_scale=float(kq),
                             window_65_100={n: float(v[win].sum() / tot_win) for n, v in hs.items()},
                             tt_over_wz_window=float(hs["TT"][win].sum() / (hs["WQQ"][win].sum() + hs["ZQQ"][win].sum())))
        fig, (ax, rx) = plt.subplots(2, 1, figsize=(6, 5), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
        bottom = np.zeros(len(BINS) - 1)
        for n in ("QCD", "TT", "ZQQ", "WQQ"):
            ax.stairs(bottom + hs[n], BINS, baseline=bottom, fill=True, color=COLORS[n], label=n + (f" ×{kq:.2f}" if n == "QCD" else ""))
            bottom = bottom + hs[n]
        ax.errorbar(0.5 * (BINS[1:] + BINS[:-1]), data, np.sqrt(data), fmt="o", ms=3, color="#0b0b0b", label="JetHT 2016GH")
        ax.set_ylabel("events / 5 GeV"); ax.legend(frameon=False, fontsize=8); ax.set_title(cname)
        rx.errorbar(0.5 * (BINS[1:] + BINS[:-1]), data / np.maximum(bottom, 1e-9), np.sqrt(data) / np.maximum(bottom, 1e-9), fmt="o", ms=3, color="#0b0b0b")
        rx.axhline(1, color="#52514e", lw=0.8); rx.set_ylim(0.7, 1.3); rx.set_xlabel("leading AK8 soft-drop mass [GeV]"); rx.set_ylabel("data/MC")
        fig.tight_layout(); fig.savefig(f"{OUT}/msd_{cname.replace('<', 'lt').replace('>', 'gt')}.png", dpi=140); plt.close(fig)
    # gen composition of MC W/Z/tt in the window, pass region
    for n in ("TT", "WQQ", "ZQQ"):
        d = s[n]; c = (d["pnmd"] > 0.9) & (d["fj_msoftdrop"] > 65) & (d["fj_msoftdrop"] < 100)
        merged = d["gen_qq_dRmax"] < 0.8
        report[f"{n}_PNMDpass_window_frac_qq_merged"] = float((d["weight"] * (c & merged)).sum() / max((d["weight"] * c).sum(), 1e-9))
    json.dump(report, open(f"{OUT}/report.json", "w"), indent=2)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
