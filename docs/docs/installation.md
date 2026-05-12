# Installation

## Requirements

- Python: 3.10+
- Package manager: uv

---

## Install [uv](https://docs.astral.sh/uv)

Follow the official instructions:

→ <https://docs.astral.sh/uv/>

!!! note
    All dependencies (e.g.,  `astropy`, `matplotlib`, `numpy`) are automatically installed by `uv` from the `uv.lock` file.

---

## Clone the Repository

```sh
git clone https://github.com/jourdanwaas/planAGN
```

```sh
cd planAGN
```

## Sync dependencies with the environment

```sh
uv sync
```