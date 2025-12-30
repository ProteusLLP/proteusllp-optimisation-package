# Installation

## Requirements

- Python 3.13 or higher
- PAL (Proteus Actuarial Library) 0.2.8 or higher

## From PyPI (Recommended)

Install via pip:

```bash
pip install proteusllp-optimisation-package
```

This will automatically install all required dependencies including PAL.

## From Source

For development or to use the latest unreleased version:

```bash
git clone https://github.com/ProteusLLP/proteusllp-optimisation-package.git
cd proteusllp-optimisation-package

# Recommended: Use devcontainer in VS Code
# Opens repo → VS Code prompts to reopen in container → runs 'pdm install' automatically

# Or install locally with PDM
pdm install
```

## Development Tools

The project uses PDM for dependency management:

```bash
pdm install        # Install all dependencies
pdm add <package>  # Add a new dependency
pdm run <command>  # Run command in PDM environment
```

## Verify Installation

```python
from pop import ObjectiveSpec, OptimizationInput
from pal import StochasticScalar

print("Proteus Optimisation Package (POP) installed successfully!")
```
