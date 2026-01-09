# AGN Habitability

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This script computes and plots a set of diagnostics for planetary atmospheres exposed to AGN winds across a span of supermassive black hole (SMBH) masses, radiative efficiencies, and wind speeds.

## Project Organization

```
├── LICENSE            <- Open-source license (MIT)
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── pyproject.toml     <- Project configuration file with package metadata for
│                         agn_habitability and configuration for tools like black
├── uv.lock            <- Lock file specifying dependencies for uv to use
│
├── docs/              <- Project documentation using mkdocs; see www.mkdocs.org for details
│
├── notebooks/         <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── reports/           <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures/       <- Generated graphics and figures to be used in reporting
│
└── agn_habitability/  <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes agn_habitability a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── main.py                 <- Stub for script code
    │
    └── model.py                <- Script to create plots for features against black hole mass
```
