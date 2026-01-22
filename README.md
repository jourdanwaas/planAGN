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
├── reports/           <- Generated outputs from scripts
│   ├── figures/       <- Generated graphics and figures as .png
│   └── results/       <- Generated .tex file outputs
│
└── agn_habitability/  <- Source code for use in this project.
    ├── __init__.py             <- Makes agn_habitability a Python module
    ├── main.py                 <- Stub for script code
    ├── model.py                <- Script to create plots across the natural range of black hole masses
    └── sample_model.py         <- Script to create plots and reports for any user-input black hole mass
```

## Getting Started

### Setting up the environment

1. Install [uv](https://docs.astral.sh/uv).
2. Clone the repository to your device.
3. Open a terminal/shell in the folder where you created the repository clone and run
   ```sh
   uv sync
   ```

### Running the code

There are two main scripts in this project:

1. `model.py` - runs the model automatically across a range of SMBH masses
2. `sample_model.py` - runs the model interactively for user-specified input values

#### Option 1: Run the full mass-range model

This will generate all plots (atmospheric heating, most probable velocity of molecules in the atmosphere, atmospheric mass loss, percentage of ozone depletion, and timescale for 90% ozone depletion) across the natural range of SMBH masses:

```sh
uv run agn_habitability/model.py
```

All resulting plots will be saved automatically under: 

```sh
reports/figures/
```

#### Option 2: Run an interactive single-galaxy model

To run the model for a specific galaxy and SMBH mass, use:

```sh
uv run agn_habitability/sample_model.py
```

The script will then prompt you for:

```sh
Enter galaxy name (or 'q' to quit):
Enter black hole mass [M_sun]:
Save plots? (y/n):
```

For example:

```sh
Enter galaxy name (or 'q' to quit): 3C 390.3
Enter black hole mass [M_sun]: 2.8e8
Save plots? (y/n): y
```

This will compute and save the corresponding plots and results for that object in:

```sh
reports/figures/3C_390.3/
reports/results/3C_390.3/
```

### Notes

- All dependencies (e.g. `astropy`, `matplotlib`, `numpy`) are automatically installed by `uv` from the `uv.lock` file.
- To run the code again in a fresh environment, simply use:

```sh
uv sync
```

- If you want to view the generated figures, you'll find them in `.png` format under `reports/figures`.
