# Wqq dataset from CMS Open Data (UL2016 NanoAODv9, 13 TeV)

A normalized replacement for the 8 TeV BACON Wqq skims, which were removed from this repo (last present in commit 75b111d). Those skims dropped every
generator weight and run/lumi branch, so tt̄ (and QCD) cannot be normalized there. Here every process
carries an absolute per-event weight, and the data luminosity is computed exactly.

## Inputs (opendata.cern.ch, read via root://eospublic.cern.ch)

| Process | Dataset (RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17) | Files used |
|---|---|---|
| Data | /JetHT/Run2016G-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD (record 30525) | all 70 |
| Data | /JetHT/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD (record 30558) | all 72 |
| tt̄ | TTToHadronic_TuneCP5_13TeV-powheg-pythia8 | 40 of 146 |
| tt̄ | TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8 | 30 of 138 |
| W | WJetsToQQ_HT-{400to600,600to800,800toInf}_TuneCP5_13TeV-madgraphMLM-pythia8 (records 69753/69755/69757) | all |
| Z | ZJetsToQQ_HT-{400to600,600to800,800toInf}_TuneCP5_13TeV-madgraphMLM-pythia8 (records 74914/74916/74918) | all |
| QCD | QCD_HT{500to700,700to1000,1000to1500,1500to2000,2000toInf}_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8 (records 63127/63140/63079/63095/63103) | 20/74, 30/61, all, all, all |

Exact file lists: `meta/files_*.txt` (truncated lists are the first N in sorted order), and `meta/jobs.txt`.

Luminosity: record 1059 (`pp_2016lumibyls.csv`, 21 MB, not stored here — download it from the record into `meta/` to rebuild; recorded lumi per LS, normtag applied) and the validated
runs JSON from record 14220 (`Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt`). The integrated
luminosity is the sum of recorded lumi over the (run, LS) pairs that appear in the processed files and
in the golden JSON. It is written to `output/summary.json`. The full-period reference values are
Run2016G 7.653 fb⁻¹ and Run2016H 8.740 fb⁻¹, with a 1.2 % uncertainty.

## Selection (`skim.py`)

- **Trigger:** `HLT_PFJet450 | HLT_AK8PFJet450 | HLT_PFHT900`, unprescaled in 2016G/H. Trimmed-mass
  triggers are excluded because they sculpt the mass. The same trigger bits are applied to MC.
- **Leading AK8 jet:** tight jetId, |η| < 2.4, pT > 525 GeV, chosen to sit above the 450 GeV trigger
  turn-on. The turn-on itself is not measured here.
- **Mass window:** 30 < m_SD < 250 GeV stored. The analysis window is 40–200 GeV.
- **Data:** golden-JSON mask, applied in `merge.py`.

## Stored per event

- **Jet kinematics:** `fj_pt`, `fj_eta`, `fj_phi`, `fj_msoftdrop` (the observable), and `fj_mass`.
  The ungroomed mass is mass-correlated, so don't use it as a feature.
- **Substructure:** τ1–τ4, N2 (`n2b1`), N3 (`n3b1`), `btagDeepB`, `nConstituents`, `lsf3`.
- **Subjets:** pt, η, φ, mass and `btagDeepB` for subjets 1 and 2.
- **Taggers, stored but flagged:**
  - `deepTag_WvsQCD` and `particleNet_WvsQCD` are not mass-decorrelated and are strongly
    mass-correlated. Do not use them as Doppio inputs.
  - `deepTagMD_WvsQCD` and `particleNetMD_{Xqq,Xcc,Xbb,QCD}` are mass-decorrelated. They are usable,
    but they are already strong supervised taggers.
- **Bookkeeping:** run, lumi, event and npv.
- **MC only:**
  - `genWeight`, `Pileup_nTrueInt` and `LHE_HT`;
  - gen matching:
    - `gen_V_pdg` (24/23/0) and `gen_V_pt` for the nearest last-copy W/Z;
    - `gen_qq_dRmax`, the largest ΔR of its quark daughters to the jet (merged if < 0.8);
    - `gen_V_from_top`, and `gen_b_dR` for the b quark from the same top;
  - `weight`, `sample_id`.

## Weights and cross sections (`merge.py`)

`weight = σ × L × genWeight / Σ genEventSumw`, where Σ runs over the Runs trees of the processed files
only. That makes the weights correct for a subset of files.

| Process | σ [pb] | Uncertainty | Source |
|---|---|---|---|
| TTToHadronic | 831.76 × 0.6741² = 377.96 | ±6 % | NNLO+NNLL σ_tt̄ (Top++, m_t = 172.5) × BR |
| TTToSemiLeptonic | 831.76 × 2 × 0.6741 × 0.3259 = 365.46 | ±6 % | as above |
| WJetsToQQ HT 400–600 / 600–800 / 800–∞ | 315.2 / 68.58 / 34.69 | ±20 % | approximate LO MadGraph values |
| ZJetsToQQ HT 400–600 / 600–800 / 800–∞ | 145.3 / 34.29 / 18.57 | ±20 % | approximate LO MadGraph values |
| QCD HT 500–700 / 700–1000 / 1000–1500 / 1500–2000 / 2000–∞ | 32100 / 6831 / 1207 / 119.9 / 25.24 | ±30 % | LO MadGraph |

- **tt̄:** the normalization is the solid one, and it is the one the Wqq fit needs as a constraint.
- **W/Z:** these cross sections are approximate and should be replaced by the official XSDB values for
  these exact samples before quoting μ as a cross-section ratio. In the Doppio fit the W/Z rate is the
  signal strength, so these numbers only set μ's units.
- **QCD:** normalization floats in rhalphabet.

## Layout (this directory)

- `<Sample>_part<k>.root` for Sample in JetHT, QCD, TT, WQQ, ZQQ: trees named `Events`, ZSTD level 22.
  - Each sample is split sequentially by entry into parts under 95 MB (GitHub's file limit).
    Concatenating the parts in k order reproduces the merged sample's raw-row order.
  - doppio's folds and the deterministic QCD unweighting are keyed on that order.
    `doppio.datasets.load_wqq_opendata_sample` reads the parts in order.
- `parts.json`: entries, bytes and MD5 per part.
- `summary.json`: luminosity, Σw, cross sections and expected yields per sample.
- `validation/`: data-vs-MC soft-drop mass plots and `report.json`.
- `scripts/`: the build, as run on subMIT. Paths in `run_skim.sh` are absolute; adapt them before reuse.
  - `skim.py`: per-file NanoAOD skim. Files are copied with xrdcp from eospublic; no grid proxy needed.
  - `run_skim.sh`: Slurm array wrapper.
  - `merge.py`: golden JSON, luminosity and weights, giving one tree per sample.
  - `validate.py`: the data-vs-MC plots and `report.json`.
  - `pack.py`: recompresses and splits the merged trees into the parts here.
- `meta/`: file lists, golden JSON, job list.

To rebuild: download the lumi CSV into `meta/`, then run
`sbatch --array=1-$(wc -l < meta/jobs.txt)%80 scripts/run_skim.sh`, then
`python scripts/merge.py && python scripts/validate.py && python scripts/pack.py <merged_dir> .`.

## Result of this production (2026-10-03)

- **Jobs:** 521 skim jobs, all completed (Slurm array 6655322).
- **Integrated luminosity:** 16.393 fb⁻¹ over 90,126 golden lumisections, with none missing from the lumi
  CSV. That equals the full Run2016G+H value.

| Sample | Selected events | Expected (weighted) | Merged size (before packing) |
|---|---|---|---|
| JetHT (data) | 5,497,461 (from 244.7M read) | — | 423 MB |
| TT (had + semilep) | 264,909 | 49,507 | 25 MB |
| WQQ | 887,396 | 74,626 | 80 MB |
| ZQQ | 523,764 | 36,338 | 48 MB |
| QCD | 8,783,178 | 6,498,707 | 710 MB |

Validation, 40–200 GeV (`validation/report.json`; plots in `validation/msd_*.png`):

| Selection | data/MC (absolute) | tt̄ / W / Z / QCD fraction in 65–100 GeV | tt̄/(W+Z) in window |
|---|---|---|---|
| Inclusive | 0.82 | 0.7 % / 2.3 % / 0.8 % / 96.2 % | 0.22 |
| τ21 < 0.35 | 0.83 | 1.7 % / 7.4 % / 2.2 % / 88.6 % | 0.17 |
| PNMD Xqq > 0.9 | 1.05 | 2.5 % / 16.2 % / 3.8 % / 77.5 % | 0.12 |

- **W/Z peaks:** clearly visible in data at the expected positions.
- **Peak normalization:** data/MC across the peak is about 0.93–0.97. That points to the approximate
  W/Z cross sections being about 5–10 % high, within their ±20 %.
- **Low mass:** below 70 GeV, data/MC is 1.1–1.17, the usual QCD-MC shape mismodelling that the
  transfer factor absorbs.
- **Merged decays in the PNMD-pass window:** 96 % of W, 92 % of Z and 89 % of tt̄ jets contain both
  quarks (ΔR < 0.8). The tt̄ contribution here is genuine merged top W's.
