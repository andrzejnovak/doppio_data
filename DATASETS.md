# Dataset Specifications

## dijet (Anomaly Detection)

**File**: `dijet/events_anomalydetection_v2.features.h5`
**Source**: CWOLAToy / LHC Olympics 2020
**Description**: Dijet invariant mass events with resonant anomaly
**Features**: 14 (jet 4-vectors + tau ratios)
**Observable**: m_jj (dijet invariant mass)
**Size**: 71 MB
**Last Updated**: 2024-10-14
**Checksum (MD5)**: `271cf5e71fc756b2a8d2b32730689bdb`

### Features
- Jet 1: px, py, pz, E
- Jet 2: px, py, pz, E
- Tau21 ratios (jet substructure)

### Usage
Used for CWOLA-style anomaly detection in dijet events. The dataset contains Standard Model background with a resonant signal injected in a specific mass window.

## bbgg (Di-Higgs)

**Source**: CWOLAToy
**Description**: bb + gamma-gamma Higgs decay events
**Observable**: m_γγ (di-photon mass)

### Background

**File**: `bbgg/bkg_bb_aa.h5`
**Description**: Background events for bb + gamma-gamma analysis
**Size**: 93 MB
**Last Updated**: 2024-10-14
**Checksum (MD5)**: `1503edb90e7365bc401ce34a6c8e19e9`

### Signal

**File**: `bbgg/sm_dihiggs.h5`
**Description**: Standard Model di-Higgs signal events
**Size**: 23 MB
**Last Updated**: 2024-10-14
**Checksum (MD5)**: `160ef2805ddd8bcafe1311ee8fb478d0`

### Features
- 10 event-level features (excluding m_γγ which is used as the observable)
- Photon kinematics
- B-jet information

### Usage
Used for CWOLA bump hunt in the di-photon mass spectrum, searching for di-Higgs production in the bb + gamma-gamma decay channel.

## Wqq (CMS 8 TeV W→qq vs QCD)

**Source**: CMS BACON ntuples (boosted hadronic V tagging)
**Description**: Substructure-based W/Z→qq tagging vs QCD multijet, used by `wqq` and `wqq_data` weak-supervision datasets
**Observable**: vjet0_msd0 (leading fatjet soft-drop mass)
**Total Size**: 664 MB across 9 split files (all under 100 MB)
**Last Updated**: 2026-05-12

### Skim recipe
- Cuts: `vjet0_pt > 300 GeV` AND `vjet0_msd0 > 20 GeV`
- Branches: 20 of 128 retained (17 substructure features + msd0 + pt + trigger)
- Compression: ROOT with ZSTD level 22
- Splits: sequential by event index, sized to fit under GitHub's 100 MB per-file limit

### Files

| File | Events | Size | MD5 |
|---|---|---|---|
| `Wqq/TT_skim.root` | 270,573 | 19 MB | `d5a9fe7b14dcd3ef7bdf0a559a0cea8f` |
| `Wqq/QCD_skim_part0.root` | 930,916 | 67 MB | `8fb1840385d1f070dc538eff2188782b` |
| `Wqq/QCD_skim_part1.root` | 930,916 | 67 MB | `40a3a7e4ce9c88336ab8b128c16eb888` |
| `Wqq/QCD_skim_part2.root` | 930,916 | 67 MB | `23bad0f359df6f84d22646262048123e` |
| `Wqq/JetHT_skim_part0.root` | 1,245,675 | 89 MB | `d9df20ed2f397c370fe3d949af331561` |
| `Wqq/JetHT_skim_part1.root` | 1,245,675 | 89 MB | `4a97cb21e3457bfd7729936ba32f0bc7` |
| `Wqq/JetHT_skim_part2.root` | 1,245,675 | 89 MB | `6734c7bf4978e79f14f4c9576771c3fa` |
| `Wqq/JetHT_skim_part3.root` | 1,245,675 | 89 MB | `b30336fdd28a38c41bc29ade9e337ce5` |
| `Wqq/JetHT_skim_part4.root` | 1,245,675 | 89 MB | `50cafbbd7350ac781fd832a50da2289b` |

See `Wqq/README.md` for full provenance, the skim script, and usage notes.

## Verifying Data Integrity

```bash
# Verify checksums
md5sum -c <<EOF
271cf5e71fc756b2a8d2b32730689bdb  dijet/events_anomalydetection_v2.features.h5
1503edb90e7365bc401ce34a6c8e19e9  bbgg/bkg_bb_aa.h5
160ef2805ddd8bcafe1311ee8fb478d0  bbgg/sm_dihiggs.h5
d5a9fe7b14dcd3ef7bdf0a559a0cea8f  Wqq/TT_skim.root
8fb1840385d1f070dc538eff2188782b  Wqq/QCD_skim_part0.root
40a3a7e4ce9c88336ab8b128c16eb888  Wqq/QCD_skim_part1.root
23bad0f359df6f84d22646262048123e  Wqq/QCD_skim_part2.root
d9df20ed2f397c370fe3d949af331561  Wqq/JetHT_skim_part0.root
4a97cb21e3457bfd7729936ba32f0bc7  Wqq/JetHT_skim_part1.root
6734c7bf4978e79f14f4c9576771c3fa  Wqq/JetHT_skim_part2.root
b30336fdd28a38c41bc29ade9e337ce5  Wqq/JetHT_skim_part3.root
50cafbbd7350ac781fd832a50da2289b  Wqq/JetHT_skim_part4.root
EOF
```
