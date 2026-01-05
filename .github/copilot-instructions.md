# GitHub Copilot Instructions for Proteus Optimizer Package

## 🔧 Essential Setup Requirements

### Devcontainer Environment
**CRITICAL**: This project uses a devcontainer with Python 3.13 and system-level packages.

**Development Environment:**
- Python 3.13 installed at system level in devcontainer
- No virtual environment needed (packages installed via `pip` directly)
- Dependencies managed through `pyproject.toml` and PDM
- PAL library installed from PyPI

### Project Structure
```
proteus-optimisation-package/
├── .devcontainer/            # Devcontainer configuration
├── .github/                  # CI/CD workflows
├── pop/                # Main package source
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration constants
│   ├── scipy_interface.py   # Optimization interface
│   ├── transforms.py        # Transformations
│   ├── efficient_frontier.py # Efficient frontier
│   └── __init__.py          # Package exports
├── tests/                   # Test suite
├── docs/                    # Documentation
├── pyproject.toml           # Package metadata & build config
└── README.md               # Package documentation
```

## 📦 Package Development

### PyPI Package
- **Package Name**: `proteus-optimizer`
- **Current Version**: 0.1.0
- **Python Requirement**: >=3.13
- **Build System**: setuptools >= 61.0

### Installation Methods
```bash
# Development (editable install from local source)
pip install -e /proteus-optimisation-package

# From PyPI
pip install proteusllp-optimisation-package
```

## 📚 Key Dependencies

### Core Libraries
- **Pydantic 2.x**: Data validation and settings management
- **PAL (Proteus Actuarial Library)**: Stochastic variables from PyPI
  - `StochasticScalar`: Basic stochastic variables
  - `ProteusVariable`: Advanced stochastic variables with methods like `.validate_freqsev_consistency()`
  - `FreqSevSims`: Frequency-severity simulations
- **NumPy 2.2+**: Numerical computations
- **SciPy 1.15+**: Optimization algorithms
- **cvxopt**: Convex optimization

### Import Patterns
```python
# PAL imports
from pal import StochasticScalar, FreqSevSims
from pal.variables import ProteusVariable

# Optimizer imports (when installed as package)
from pop import ObjectiveSpec, OptimizationInput, OptimizationResult
from pop.config import OptimizationDirection, MetricType
```

## 🚀 Current Implementation Status

### Phase 1: ✅ COMPLETE - Python 3.13 Migration & Package Setup
- Migrated from Python 3.11 to Python 3.13
- Updated to use PAL from PyPI (v0.2.8+)
- Updated to use `ProteusVariable.validate_freqsev_consistency()` method
- Created PyPI package structure with pyproject.toml

### Phase 2: 📋 PLANNED - Testing and CI/CD
- Run full test suite in package context
- Set up GitHub Actions for automated testing
- Configure PyPI publishing workflow

### Phase 3: 📋 PLANNED - PyPI Publication
- Publish initial version to PyPI
- Update dashboard to use published package
- Documentation and versioning strategy

## 🔍 Development Guidelines

### Testing Strategy
- Use real PAL objects in tests (not mocks when possible)
- Validate Pydantic error messages are helpful
- Test both success and failure cases
- Run tests with: `python3 -m pytest tests/ -v`

### Code Quality
- Use type hints throughout
- Comprehensive docstrings for all public functions
- Follow Pydantic best practices
- Clear error messages with helpful suggestions
- Format with Ruff: `ruff format .`
- Lint with Ruff: `ruff check .`

### Terminal Commands
- Use `pdm run` prefix for Python commands (PDM manages virtual environment)
- Use absolute paths when possible
- PDM automatically activates .venv in devcontainer
- Install package: `pdm install`
- Add dependencies: `pdm add <package>`

## 🎯 Common Tasks

### Running Tests
```bash
pdm run pytest tests/ -v
# or
make test
```

### Building Package
```bash
pdm build
# or
make build
```

### Installing Package Locally
```bash
pdm install
```

### Linting and Formatting
```bash
pdm run ruff check .
pdm run ruff format .
# or
make lint
make format
```

## ⚠️ Common Pitfalls to Avoid

1. **PAL API changes**: Use `ProteusVariable` (not `ProteusStochasticVariable`), call `.validate_freqsev_consistency()` method
2. **Import naming**: Check current PAL documentation for correct class names
3. **File editing**: Use large context windows to avoid corruption
4. **Package structure**: Keep exports in `__init__.py` clean and organized
5. **PAL Installation**: Package now uses PAL 0.2.8+ from PyPI

## 📖 Architecture Notes

### Domain-Agnostic Design
All models use Pydantic for:
- Automatic validation
- Type coercion
- Serialization
- Clear error messages
- Documentation generation

### Package Purpose
This package provides the core optimization engine for stochastic portfolio optimization. It is designed to be:
- **Standalone**: Can be used independently of the dashboard
- **Generic**: Works with any PAL stochastic variables
- **Extensible**: Easy to add new objective functions and constraints
- **Well-tested**: Comprehensive test suite included

This file ensures consistent development practices across all GitHub Copilot interactions.
