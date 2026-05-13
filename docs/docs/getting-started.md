Getting Started
===============

## Overview

Active galactic nuclei (AGN) emit powerful ultrafast outflows (UFOs) that carry significant energy into their host galaxies. These outflows may interact with planetary atmospheres, depositing energy which drives significant increase in atmospheric temperature, enhancing conditions for escape and depletion of ozone.

This code models these processes using parameterizations for AGN outflows and evaluates their effects across a wide range of supermassive black hole (SMBH) masses and galactocentric distances.

The specifications of the diagnostics can be found in the [output](output.md) section.

## Installation

### Requirements

- Python: 3.10+
- Package manager: [uv](https://docs.astral.sh/uv)

---

### Install [uv](https://docs.astral.sh/uv)

Follow the official instructions:

→ <https://docs.astral.sh/uv/>

---

### Clone the Repository

```sh
git clone https://github.com/jourdanwaas/planAGN
```

### Set Up the Environment

In the `planAGN` directory, run the following line to sync dependencies:

```sh
uv sync
```

!!! note
    All dependencies (e.g.,  `astropy`, `matplotlib`, `numpy`) are automatically installed by `uv` from the `uv.lock` file.

This can also be used to run the code again in a fresh environment.