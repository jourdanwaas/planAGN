# planAGN

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This model computes and plots a set of diagnostics for planetary atmospheres exposed to AGN winds across a span of supermassive black hole (SMBH) masses and at various distances from the central SMBH.

## Project Organization

```
├── LICENSE            ← Open-source license (MIT)
├── Makefile           ← Makefile
├── README.md          ← The top-level README for developers using this project.
├── pyproject.toml     ← Project configuration file with package metadata for
│                        planAGN
├── uv.lock            ← Lock file specifying dependencies for uv to use
│
├── docs/              ← Project documentation using mkdocs; see www.mkdocs.org for details
│
├── notebooks/         ← Jupyter notebooks (coming soon). 
│
├── reports/           ← Generated outputs from scripts
│   ├── figures/       ← Generated graphics and figures as .png files
│   └── results/       ← Generated .tex file outputs
│
└── planAGN/  ← Source code for use in this project.
    ├── __init__.py             ← Makes planAGN a Python module
    ├── main.py                 ← Stub for script code (currently can be used as a test)
    ├── model.py                ← Script to create plots across the natural range of black hole masses
    └── sample_model.py         ← Script to create plots and reports for any user-input black hole mass
```

For documentation, please see the docs at:

[https://jourdanwaas.github.io/planAGN/](https://jourdanwaas.github.io/planAGN/)
