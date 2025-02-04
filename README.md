# AirTrafficSim

[![image](https://img.shields.io/pypi/v/airtrafficsim.svg)](https://pypi.python.org/pypi/airtrafficsim)
[![image](https://img.shields.io/pypi/l/airtrafficsim.svg)](https://pypi.python.org/pypi/airtrafficsim)
[![image](https://img.shields.io/pypi/pyversions/airtrafficsim.svg)](https://pypi.python.org/pypi/airtrafficsim)
[![image](https://img.shields.io/pypi/status/airtrafficsim)](https://pypi.python.org/pypi/airtrafficsim)

<img src="docs/assets/img/Logo-full.png" width=50% />

AirTrafficSim is a lightweight collection of tools for air traffic management research.

This branch (`v0.2`) contains the rewrite of the older `v0.1`[^1] version.

It aims to be significantly more accessible, with absolutely minimal dependencies by default. Extra features (e.g. full web-based simulation environment) must be enabled manually with feature flags.

## Features

- support for modern automatic differentiation (via JAX)
- support for the [Array API](https://data-apis.org/array-api): Numpy, JAX, PyTorch, CuPy arrays can be passed into functions
  - partial support for `polars.Expr` with plugin
- BADA3 ISA atmosphere model
- thermodynamic calculations

## Installation

`v0.2` is currently under heavy development and not considered stable. For the latest alpha version:

```sh
pip install airtrafficsim
```

For the latest bleeding-edge version:

```sh
pip install "https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/archive/dev.zip"
```

### Feature Flags

Using the command above will install a version with very minimal footprint. Depending on your use case, you can select one or more optional dependencies:

- `all`: install all optional dependencies
- `polars`: support for polars DataFrame (used in simulation and postprocessing third party data)
- `networking`: support for downloading data from external third party sources
- `era5`: support for parsing NetCDF for Google ARCO ERA5.
- `jax`: support for automatic differentiation
- `plot`: utils for nicer plotting

For example:

```sh
pip install "airtrafficsim[networking,polars]"
```

## Development

```sh
git clone https://github.com/HKUST-OCTAD-LAB/AirTrafficSim -b dev --depth=1
cd AirTrafficSim
uv venv
uv sync --all-extras --all-groups
```

To run scripts:

```sh
uv run examples/autodiff.py
```

Alternatively, activate your virtualenv:

```sh
source .venv/bin/activate
python3 examples/autodiff.py
```

### Documentation

```sh
uv run mkdocs serve
```

Then, navigate to http://127.0.0.1:8000/AirTrafficSim/.

### Contributing

1. Follow [Black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) style. 
2. Prefer pure functions over deep inheritance hierarchies.
3. Use typed code whenever possible.

We use the following tools to check the style on each push:

- [Ruff](https://github.com/astral-sh/ruff) for linting,
- [MyPy](https://github.com/python/mypy) for type checking 

Locally, run the following before committing:

```sh
chmod +x ./scripts/style-check.sh
./scripts/style-check.sh
```

Recommended VSCode extensions: `charliermarsh.ruff`, `matangover.mypy`, `usernamehw.errorlens`, `ms-toolsai.jupyter`

[^1]: The latest commit can be viewed [here](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/commit/7a3c3249e602ad17c4b27c7bf900e571d9f7feea). It is considered deprecated and will not receieve futher updates.

## License

Unlike `v0.1` (GPLv3), this branch is licensed under the more permissive [MIT License](./LICENSE).