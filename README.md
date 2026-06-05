# planAGN

[![cookiecutter badge](https://img.shields.io/badge/CCDS-328F97?logo=cookiecutter)](https://cookiecutter-data-science.drivendata.org/) [![docs badge](https://img.shields.io/badge/docs-blue.svg)](https://jourdanwaas.github.io/planAGN) [![DOI](https://zenodo.org/badge/1129314961.svg)](https://doi.org/10.5281/zenodo.20561197)

This model computes and plots a set of diagnostics for planetary atmospheres exposed to AGN winds across a span of supermassive black hole (SMBH) masses and at various distances from the central SMBH.

## Project Organization

```
├── LICENSE            ← Open-source license (MIT)
├── Makefile           ← Makefile
├── README.md          ← The top-level README
├── pyproject.toml     ← Project configuration file with package metadata for planAGN
├── uv.lock            ← Lock file specifying dependencies for uv to use
│
├── docs/              ← Documentation
│
├── notebooks/         ← Jupyter notebooks (coming soon).
│
├── reports/           ← Generated outputs from scripts
│   ├── figures/       ← Generated graphics and figures as .png files
│   └── results/       ← Generated .tex file outputs
│
└── planAGN/  ← Source code
    ├── __init__.py             ← Makes planAGN a Python module
    ├── main.py                 ← Stub for script code (currently can be used as a test)
    ├── model.py                ← Script to create plots across the natural range of black hole masses
    └── sample_model.py         ← Script to create plots and reports for any user-input black hole mass
```
