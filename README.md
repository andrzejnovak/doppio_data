# Doppio Data Repository

Datasets used by the CWOLA bump hunt analysis framework.

## Contents

- **dijet**: Anomaly Detection dijet events from LHC Olympics 2020
- **bbgg**: Di-Higgs bb + gamma-gamma events
- **Wqq**: CMS 8 TeV W→qq vs QCD substructure ROOT skims (split into ≤100 MB chunks)

## Usage

This repo is used as a git submodule in the [doppio](https://github.com/anovak/doppio) project.

### As a Submodule

```bash
# Clone doppio with submodules
git clone --recurse-submodules https://github.com/anovak/doppio.git

# Or initialize submodules after cloning
cd doppio
git submodule update --init --recursive
```

### Standalone Usage

```python
import h5py

# Load dijet data
with h5py.File('dijet/events_anomalydetection_v2.features.h5', 'r') as f:
    data = f['data'][:]

# Load bbgg data
with h5py.File('bbgg/bkg_bb_aa.h5', 'r') as f:
    background = f['data'][:]

with h5py.File('bbgg/sm_dihiggs.h5', 'r') as f:
    signal = f['data'][:]
```

## Data Integrity

See [DATASETS.md](DATASETS.md) for checksums and detailed dataset information.

## License

Data from LHC Olympics 2020 and related sources. See individual dataset documentation for specific licenses and citations.

## Citation

If you use these datasets, please cite the original sources:
- LHC Olympics 2020: https://lhco2020.github.io/homepage/
