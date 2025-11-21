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

## Verifying Data Integrity

```bash
# Verify checksums
md5sum -c <<EOF
271cf5e71fc756b2a8d2b32730689bdb  dijet/events_anomalydetection_v2.features.h5
1503edb90e7365bc401ce34a6c8e19e9  bbgg/bkg_bb_aa.h5
160ef2805ddd8bcafe1311ee8fb478d0  bbgg/sm_dihiggs.h5
EOF
```
