# Di-Higgs (bb + gamma-gamma) Dataset

## Overview

Di-Higgs production events in the bb + gamma-gamma decay channel, used for CWOLA bump hunt analysis.

## Files

- `bkg_bb_aa.h5` (93 MB) - Background events
- `sm_dihiggs.h5` (23 MB) - Standard Model di-Higgs signal events

## Description

This dataset contains simulated events for di-Higgs production analysis:

- **Features (10 total)**: Event-level features including photon kinematics and b-jet information (excluding m_γγ)
- **Observable**: Di-photon invariant mass (m_γγ)

## Signal vs Background

- **Background** (`bkg_bb_aa.h5`): Standard Model background processes producing bb + gamma-gamma final states
- **Signal** (`sm_dihiggs.h5`): Resonant di-Higgs production (HH → bb + gamma-gamma)

## Usage in doppio

```python
from datasets import load_dataset

dataset = load_dataset('bbgg')
X_train = dataset.train['X']  # Features
obs_train = dataset.train['obs']  # Di-photon mass
```

## Analysis Strategy

The CWOLA method performs a bump hunt in the di-photon mass spectrum to discover the di-Higgs signal without using labels during training.

## References

- Di-Higgs production at LHC
- ATLAS/CMS di-Higgs searches
