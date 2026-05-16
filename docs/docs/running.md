Running the Models
===============

There are two main scripts in this project:

1. `model.py` - runs the model automatically across a range of SMBH masses
2. `sample_model.py` - runs the model interactively for user-specified input values

!!! tip
    Use the interactive model for quick testing.

---

## 1. Natural Mass Range Model


```sh
uv run planAGN/model.py
```

This runs the model across the natural range of SMBH masses and generates results for the following:

- Atmospheric heating
- Most probable molecular velocity
- Atmospheric mass loss
- Ozone depletion percentage
- Timescale for 90% ozone depletion

---

## 2. Single Galaxy Model

To run the model for a specific galaxy and SMBH mass, use:

```sh
uv run planAGN/sample_model.py
```

The script will then prompt you for:

```sh
Enter galaxy name (or 'q' to quit):
Enter black hole mass [M_sun]:
Save plots? (y/n):
```

### Input Parameters

Galaxy Name

- Description: Assigns the corresponding folder and file name for all results related to a given object

BH Mass

- Units: Solar masses (M<sub>☉</sub>)
- Typical range: $10^6 - 10^{10} M_{\odot}$

Save Option

- `y`: saves plots and results
- `n`: runs without saving

#### Single Galaxy Example

```sh
Enter galaxy name (or 'q' to quit): 3C 390.3
Enter black hole mass [M_sun]: 2.8e8
Save plots? (y/n): y
```

This script will generate and locally save results for the radio galaxy 3C 390.3, which contains a central SMBH with a mass of $2.8 \times 10^8 M_{\odot}$.

!!! note
    The code will produce a compatible file name for the object, therefore inputting a space into the interactive prompt is acceptable.
