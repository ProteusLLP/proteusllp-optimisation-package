<!--pytest-codeblocks:skipfile-->
# Proteus Optimisation Package Style Guide

This document outlines the coding standards and style guidelines for the Proteus Optimisation Package (POP).

## Code Style

- **Line Length**: 88 characters (following Black's default)
- **Python Version**: 3.13+
- **Import Sorting**: Automatic via ruff (isort rules)
- **Code Formatting**: Automatic via ruff formatter
- **Whitespace**: No trailing whitespace at end of lines
- **Blank Lines**: No unnecessary blank lines (follow PEP 8 guidelines)

## Type Annotations

- **Required**: All public functions, methods, and classes must have complete type annotations
- **Authority**: Type hints are the authoritative source for type information
- **No Duplication**: Do not repeat type information in docstrings

### Type Ignore Comments

Only use `# type: ignore` when there's a legitimate reason. Always:
1. Use specific error codes, not broad ignores
2. Document why the ignore is necessary
3. Consider if there's a better solution (type assertion, protocol, etc.)

**Good:**
```python
# scipy-stubs has incomplete type information for minimize()
result = scipy.optimize.minimize(...)  # type: ignore[misc]

# pydantic uses runtime type generation that mypy can't analyze
class Config(BaseModel):  # type: ignore[misc]
    value: Any
```

**Bad:**
```python
result = some_function()  # type: ignore  # Too broad, no explanation

# Unnecessary ignore - fix the actual type issue instead
x = cast_value()  # type: ignore
```

**Legitimate reasons for type ignores:**
- Incomplete or incorrect type stubs in third-party libraries
- Known limitations in the type checker (e.g., complex generics)
- Dynamic code that's correct but hard for static analysis to understand

```python
# Good
def optimize_portfolio(objectives: list[ObjectiveSpec], constraints: list[Constraint]) -> OptimizationResult:
    """Optimize portfolio allocation under given objectives and constraints.
    
    Args:
        objectives: List of optimization objectives to satisfy
        constraints: List of constraints on the solution space
    
    Returns:
        Optimization result with optimal weights and metrics
    """
    return run_optimization(objectives, constraints)

# Bad - type information duplicated in docstring
def optimize_portfolio(objectives: list[ObjectiveSpec], constraints: list[Constraint]) -> OptimizationResult:
    """Optimize portfolio allocation under given objectives and constraints.
    
    Args:
        objectives (list[ObjectiveSpec]): List of optimization objectives
        constraints (list[Constraint]): List of constraints
    
    Returns:
        OptimizationResult: Optimization result with optimal weights
    """
    return run_optimization(objectives, constraints)
```

## Comments

- **Purpose**: Comments should explain WHY, not WHAT the code does
- **Line Length**: Must not exceed 88 characters per line
- **Quality**: The code itself shows what it does - comments that repeat this are redundant noise
- **Good comments explain**:
  - Business logic and domain-specific rules
  - Non-obvious design decisions
  - Edge cases and their handling
  - Performance or numerical stability considerations

```python
# Bad - explains WHAT (redundant)
# Loop through all weights
for weight in weights:
    process(weight)

# Good - explains WHY
# Normalize weights iteratively to handle floating point precision issues
# that can cause sum(weights) != 1.0 after constraint projection
for iteration in range(max_iterations):
    weights = weights / weights.sum()
    if abs(weights.sum() - 1.0) < tolerance:
        break
```

## Docstrings

- **Style**: Google-style docstrings
- **Required**: All public modules, classes, functions, and methods
- **Required**: Test functions should have docstrings explaining what they test
- **No Types**: Do not include type information in docstrings (use type hints instead)

### Function/Method Docstrings

```python
def compute_efficient_frontier(
    returns: StochasticScalar,
    risk_measure: MetricType,
    n_points: int = 50
) -> EfficientFrontier:
    """Compute the efficient frontier for a portfolio optimization problem.
    
    Traces out the Pareto-optimal trade-off between expected return and risk
    by solving optimization problems at different risk-return target points.
    
    Args:
        returns: Stochastic variable representing portfolio returns
        risk_measure: Risk metric to minimize (e.g., VaR, CVaR, variance)
        n_points: Number of points to compute along the frontier
    
    Returns:
        Efficient frontier object containing optimal portfolios
    
    Raises:
        OptimizationError: If optimization fails to converge
        ValueError: If n_points < 2
    """
```

### Class Docstrings

```python
class OptimizationEngine:
    """Core optimization engine for stochastic portfolio optimization.
    
    Provides methods for solving portfolio optimization problems with
    multiple objectives, constraints, and risk measures. Supports both
    analytical and numerical gradient computation.
    
    Attributes:
        algorithm: Optimization algorithm to use (e.g., 'SLSQP', 'trust-constr')
        max_iterations: Maximum number of optimization iterations
        tolerance: Convergence tolerance for optimization
    """
```

### Test Docstrings

```python
def test_optimization_with_equality_constraint():
    """Test that optimization respects equality constraints on weights."""

def test_efficient_frontier_monotonicity():
    """Test that efficient frontier has monotonically increasing risk-return."""
```

## Security

- **No Secrets**: Never commit API keys, passwords, or sensitive data
- **Input Validation**: Validate all external inputs using Pydantic models
- **Numerical Stability**: Check for division by zero, overflow, and NaN values

## Static Analysis Tools

The following tools are configured and must pass in CI:

- **ruff**: Linting, formatting, import sorting, docstring validation
- **mypy**: Type checking with strict mode
- **pytest**: Unit testing with coverage requirements

## VS Code Configuration

Install these extensions for consistent development experience:

- **Ruff** (`charliermarsh.ruff`) - Primary linter and formatter
- **Pylance** (`ms-python.pylance`) - Type checking and IntelliSense
- **Python** (`ms-python.python`) - Core Python support

The project includes `.devcontainer/` configuration with tool settings that match CI.

## Enforcement

All static analysis checks must pass before code can be merged. The CI pipeline will:
1. Run ruff for linting and formatting checks
2. Run mypy for type checking
3. Run pytest for unit tests with coverage
4. Build the package to verify distribution readiness

Use `make check` locally to ensure compliance before pushing.
