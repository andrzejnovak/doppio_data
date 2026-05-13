# Wqq Dataset (CMS 8 TeV W→qq vs QCD)

## Overview

CMS BACON ntuples for boosted hadronic V (W/Z) tagging vs QCD multijet background, used for the `wqq` and `wqq_data` weak-supervision datasets in doppio.

## Files

| File | Events | Size | MD5 |
|---|---|---|---|
| `TT_skim.root` | 270,573 | 19 MB | `d5a9fe7b14dcd3ef7bdf0a559a0cea8f` |
| `QCD_skim_part0.root` | 930,916 | 67 MB | `8fb1840385d1f070dc538eff2188782b` |
| `QCD_skim_part1.root` | 930,916 | 67 MB | `40a3a7e4ce9c88336ab8b128c16eb888` |
| `QCD_skim_part2.root` | 930,916 | 67 MB | `23bad0f359df6f84d22646262048123e` |
| `JetHT_skim_part0.root` | 1,245,675 | 89 MB | `d9df20ed2f397c370fe3d949af331561` |
| `JetHT_skim_part1.root` | 1,245,675 | 89 MB | `4a97cb21e3457bfd7729936ba32f0bc7` |
| `JetHT_skim_part2.root` | 1,245,675 | 89 MB | `6734c7bf4978e79f14f4c9576771c3fa` |
| `JetHT_skim_part3.root` | 1,245,675 | 89 MB | `b30336fdd28a38c41bc29ade9e337ce5` |
| `JetHT_skim_part4.root` | 1,245,675 | 89 MB | `50cafbbd7350ac781fd832a50da2289b` |
| `WQQ_sh.root` (signal MC) | 125,418 | 32 MB | `a4834a3a7f1f79d7f33da2dff0625deb` |
| `WQQ_s.root` (signal demo) | 749 | 237 KB | `04f629fe7b66654a1dd27035b8e53969` |
| `ZQQ_sh.root` (signal MC) | 107,867 | 28 MB | `b040739ad75d20bab0e48636bdfeb9d0` |
| `ZQQ_s.root` (signal demo) | 589 | 197 KB | `eeb75f579f38195aace91d692f88e3d9` |
| **Total** | **9,324,099** | **724 MB** | — |

The QCD/JetHT/TT skims use ZSTD level-22 compression and stay under the 100 MB GitHub per-file limit. The signal MC files are the original BACON ntuples (125 branches, default ROOT compression) — they were already small enough not to need re-skimming.

## Sample descriptions

- **TT** — tt̄ Monte Carlo (top quark pair production background, hadronic W's at modest pT)
- **QCD** — QCD multijet Monte Carlo (the dominant fatjet background)
- **JetHT** — CMS data primary dataset (unlabeled real collider events used as the training target for CWoLa-style weak supervision)
- **WQQ** — W→qq signal MC; `_sh` is the full sample (125k events), `_s` is a tiny dev subset (749 events) used as the loader's `WQQ_FALLBACK_SIGNAL_FILE`
- **ZQQ** — Z→qq signal MC; same layout as WQQ (`_sh` full, `_s` dev subset). The Z hadronic resonance sits at ~91 GeV vs the W at ~80 GeV in the `vjet0_msd0` observable.

## Skim provenance

The original BACON ntuples (~3 GB across QCD + TT + JetHT alone) were skimmed with two cuts and a branch list reduction:

1. **Event cuts**: `vjet0_pt > 300` AND `vjet0_msd0 > 20`
2. **Branches kept** (20 of 128): the 17 substructure features used by `doppio.datasets.load_wqq*` (`vjet0_csv`, `vjet0_t1/t2/t3`, `vjet0_pullAngle`, `vjet0_sj{1,2}_{csv,q,z}`, `vjet0_c2b{0,0P2,0P5,1P0,2P0}`, `vjet0_qjet`) plus `vjet0_msd0` (observable), `vjet0_pt` (kinematic cut), and `trigger` (HLT bitmask used by aopatton's loader).
3. **Splits**: each output is sequentially split by event index into N parts to keep individual files under 100 MB. QCD into 3 parts (~67 MB each), JetHT into 5 parts (~89 MB each), TT as one file (already small after cuts).

These cuts retain ~100% of QCD and JetHT events (the upstream producer already applied looser preselection that subsumes the cut) and drop ~75% of TT (which had events down to pT 200). All branches needed by aopatton's loader are preserved; only unused branches (lepton kinematics, AK4 jet info, MET, generator info, BDT scores) are dropped.

The skim script is included as `make_wqq_skim.py` for reproducibility:

```bash
pixi run python Wqq/make_wqq_skim.py --src-dir <path-to-original-data> --out-dir Wqq
```

## Usage with doppio

The doppio Wqq loaders (`wqq`, `wqq_data` in `doppio/datasets.py`) expect this directory at `./doppio_data/Wqq` and will pick up the parts via glob:

```bash
# Weak supervision (CWoLa) on JetHT data
pixi run python train.py --config configs/reference/wqq_data_cwola.yaml

# Pretrain on QCD MC, fine-tune on data
pixi run python train.py --config configs/reference/wqq_pretrain_cwola_disco.yaml
```

The loader currently expects single files; update the loader to glob over `*_part*.root` to read these splits transparently (see follow-up PR in `andrzejnovak/doppio`).

## Verifying integrity

```bash
md5sum -c <<EOF
d5a9fe7b14dcd3ef7bdf0a559a0cea8f  Wqq/TT_skim.root
8fb1840385d1f070dc538eff2188782b  Wqq/QCD_skim_part0.root
40a3a7e4ce9c88336ab8b128c16eb888  Wqq/QCD_skim_part1.root
23bad0f359df6f84d22646262048123e  Wqq/QCD_skim_part2.root
d9df20ed2f397c370fe3d949af331561  Wqq/JetHT_skim_part0.root
4a97cb21e3457bfd7729936ba32f0bc7  Wqq/JetHT_skim_part1.root
6734c7bf4978e79f14f4c9576771c3fa  Wqq/JetHT_skim_part2.root
b30336fdd28a38c41bc29ade9e337ce5  Wqq/JetHT_skim_part3.root
50cafbbd7350ac781fd832a50da2289b  Wqq/JetHT_skim_part4.root
a4834a3a7f1f79d7f33da2dff0625deb  Wqq/WQQ_sh.root
04f629fe7b66654a1dd27035b8e53969  Wqq/WQQ_s.root
b040739ad75d20bab0e48636bdfeb9d0  Wqq/ZQQ_sh.root
eeb75f579f38195aace91d692f88e3d9  Wqq/ZQQ_s.root
EOF
```
