Outputs
===============

## Diagnostic Features

The model focuses on five primary atmospheric diagnostics:

- Atmospheric heating
- Most probable velocity of molecules in the atmosphere
- Atmospheric mass loss
- Percentage of ozone depletion
- Timescale for 90% ozone depletion

These features are contained in plotted outputs.

For any specific galaxy, with a given SMBH mass input, the model computes the following in addition to the above plots:

- Maximum distance of influence where atmospheric escape arises from thermal heating
- Maximum distance of influence for energy-limited hydrodynamic-like escape
- Maximum distance for major ozone depletion (90% loss) due to nitrogen oxide formation

---

## 1. Natural Mass Range Model

All resulting plots will be saved automatically under:

```sh
reports/figures/natural mass range/
```

---

## 2. Single Galaxy Model

### Figures

- Location: `reports/figures/<galaxy_name>/`
- Format: `.png`

Running the sample model will generate a folder in this location based on the user-input galaxy name, in which the respective figures for each diagnostic feature are located and named appropriately.

For example, the atmospheric heating plot for 3C 390.3 can be found in `reports/figures/3C_390.3/` as `heating__3C_390.3.png`.

### Results

- Location: `reports/results/<galaxy_name>/`
- Format: `.tex`
