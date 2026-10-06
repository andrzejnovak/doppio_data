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

## WqqOpenData (CMS Open Data 2016, 13 TeV, W/Z→qq vs QCD)

**Source**: CMS Open Data, UL2016 NanoAODv9 (JetHT Run2016G+H, 16.4 fb⁻¹; TTToHadronic/SemiLeptonic, W/ZJetsToQQ HT-binned, QCD HT-binned)
**Description**: Leading AK8 jet (pT > 525 GeV) substructure for W/Z→qq tagging vs QCD, with absolute per-event MC weights (σ × L × genWeight / Σw) and gen matching; used by the `wqq_opendata*` datasets in doppio
**Observable**: `fj_msoftdrop` (leading AK8 soft-drop mass), analysis window 40–200 GeV
**Total Size**: 1.05 GB across 16 files (each < 95 MB)
**Last Updated**: 2026-10-06
**Replaces**: the 8 TeV BACON `Wqq/` skims, which carried no generator weights (tt̄ could not be normalised). They were removed; they are last present in commit 75b111d.

### Layout
- **Parts.** `<Sample>_part<k>.root`, trees named `Events`, ZSTD level 22.
- **Order.** Each sample is split sequentially by entry, so concatenating the parts in `k` order restores the raw-row order. doppio's folds are keyed on that order.
- **Rebuild.** Build scripts, file lists and provenance are in `WqqOpenData/README.md` and `WqqOpenData/scripts/`. `WqqOpenData/parts.json` holds per-part entries, bytes and MD5s.

### Files

| File | Events | Size | MD5 |
|---|---|---|---|
| `WqqOpenData/JetHT_part0.root` | 1,314,783 | 82.3 MB | `4acddb9d62029e86667ca2a930b17fa2` |
| `WqqOpenData/JetHT_part1.root` | 1,314,783 | 82.2 MB | `5497552c940feae4db505af87ffb4235` |
| `WqqOpenData/JetHT_part2.root` | 1,314,783 | 82.5 MB | `419838a262da72a997babc82a888856a` |
| `WqqOpenData/JetHT_part3.root` | 1,314,783 | 82.6 MB | `176adce53f8c53a921565062103fea6f` |
| `WqqOpenData/JetHT_part4.root` | 238,329 | 15.4 MB | `281a9be427f8e61dade422b840533dca` |
| `WqqOpenData/QCD_part0.root` | 1,236,510 | 82.0 MB | `e1b2141a6b3f3a57709bdec1e937361d` |
| `WqqOpenData/QCD_part1.root` | 1,236,510 | 81.2 MB | `8939d9487076e67851b38e436f36131d` |
| `WqqOpenData/QCD_part2.root` | 1,236,510 | 81.4 MB | `98f53e3931aabec23c82002edd8a4d17` |
| `WqqOpenData/QCD_part3.root` | 1,236,510 | 81.1 MB | `2f92a18e5dc51fead484cb37ab21ae13` |
| `WqqOpenData/QCD_part4.root` | 1,236,510 | 81.0 MB | `06694b8f4801df237cb3439882c7c1f2` |
| `WqqOpenData/QCD_part5.root` | 1,236,510 | 81.6 MB | `69e1830b0f609228958c4889073ae4ab` |
| `WqqOpenData/QCD_part6.root` | 1,236,510 | 82.3 MB | `b8c532f70b88fd64373290ee136b12a0` |
| `WqqOpenData/QCD_part7.root` | 127,608 | 8.8 MB | `e465dbdb905690f78016d19233746f8e` |
| `WqqOpenData/TT_part0.root` | 264,909 | 21.5 MB | `45e57b50f212f0be5604d5d13fad7594` |
| `WqqOpenData/WQQ_part0.root` | 887,396 | 66.8 MB | `02fd488afdaccc80adaa6b32f059b4a4` |
| `WqqOpenData/ZQQ_part0.root` | 523,764 | 39.7 MB | `80f666cfe4bbf9b2e538881caec327fc` |

See `WqqOpenData/README.md` for record IDs, cross sections, luminosity, selection and validation.

## Verifying Data Integrity

```bash
# Verify checksums
md5sum -c <<EOF
271cf5e71fc756b2a8d2b32730689bdb  dijet/events_anomalydetection_v2.features.h5
1503edb90e7365bc401ce34a6c8e19e9  bbgg/bkg_bb_aa.h5
160ef2805ddd8bcafe1311ee8fb478d0  bbgg/sm_dihiggs.h5
4acddb9d62029e86667ca2a930b17fa2  WqqOpenData/JetHT_part0.root
5497552c940feae4db505af87ffb4235  WqqOpenData/JetHT_part1.root
419838a262da72a997babc82a888856a  WqqOpenData/JetHT_part2.root
176adce53f8c53a921565062103fea6f  WqqOpenData/JetHT_part3.root
281a9be427f8e61dade422b840533dca  WqqOpenData/JetHT_part4.root
e1b2141a6b3f3a57709bdec1e937361d  WqqOpenData/QCD_part0.root
8939d9487076e67851b38e436f36131d  WqqOpenData/QCD_part1.root
98f53e3931aabec23c82002edd8a4d17  WqqOpenData/QCD_part2.root
2f92a18e5dc51fead484cb37ab21ae13  WqqOpenData/QCD_part3.root
06694b8f4801df237cb3439882c7c1f2  WqqOpenData/QCD_part4.root
69e1830b0f609228958c4889073ae4ab  WqqOpenData/QCD_part5.root
b8c532f70b88fd64373290ee136b12a0  WqqOpenData/QCD_part6.root
e465dbdb905690f78016d19233746f8e  WqqOpenData/QCD_part7.root
45e57b50f212f0be5604d5d13fad7594  WqqOpenData/TT_part0.root
02fd488afdaccc80adaa6b32f059b4a4  WqqOpenData/WQQ_part0.root
80f666cfe4bbf9b2e538881caec327fc  WqqOpenData/ZQQ_part0.root
EOF
```
