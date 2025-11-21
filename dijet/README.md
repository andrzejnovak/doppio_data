# Dijet Anomaly Detection Dataset

## Overview

Dijet invariant mass events from the LHC Olympics 2020 Anomaly Detection challenge.

## File

- `events_anomalydetection_v2.features.h5` (71 MB)

## Description

This dataset contains simulated proton-proton collision events with two jets. The data includes:

- **Features (14 total)**:
  - Jet 1 four-vector: px, py, pz, E
  - Jet 2 four-vector: px, py, pz, E
  - Tau21 jet substructure variables

- **Observable**: Dijet invariant mass (m_jj)

## Signal

A resonant anomaly (new particle) is injected in the dataset at a specific mass window. The CWOLA method is used to discover this signal without direct supervision.

## Usage in doppio

```python
from datasets import load_dataset

dataset = load_dataset('rnd_d')
X_train = dataset.train['X']  # Features
obs_train = dataset.train['obs']  # Dijet mass
```

## References

- LHC Olympics 2020: https://lhco2020.github.io/homepage/
- Original dataset: https://zenodo.org/record/2629073
