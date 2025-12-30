# Quick Start

This guide will get you started with the Proteus Optimisation Package (POP) in minutes.

## Basic Example

```python
from pal import StochasticScalar
from pop import ObjectiveSpec, OptimizationInput, scipy_optimize
from pop.config import MetricType, OptimizationDirection

# Create stochastic variables for two assets
returns_a = StochasticScalar(mean=0.08, std=0.15, size=10000)
returns_b = StochasticScalar(mean=0.06, std=0.10, size=10000)

# Calculate portfolio returns as weighted sum
def portfolio_returns(weights):
    return weights[0] * returns_a + weights[1] * returns_b

# Define optimization objective: maximize expected return
objective = ObjectiveSpec(
    metric_type=MetricType.MEAN,
    direction=OptimizationDirection.MAXIMIZE,
    target_value=None
)

# Create optimization input
opt_input = OptimizationInput(
    objectives=[objective],
    n_assets=2,
    initial_weights=[0.5, 0.5],
    equality_constraints=[],  # Weights sum to 1 enforced by default
    inequality_constraints=[],
    box_constraints=[(0.0, 1.0)] * 2  # Weights between 0 and 1
)

# Run optimization
result = scipy_optimize(
    portfolio_returns,
    opt_input,
    method="SLSQP"
)

print(f"Optimal weights: {result.optimal_weights}")
print(f"Success: {result.success}")
print(f"Message: {result.message}")
```

## Computing Efficient Frontier

```python
from pop.efficient_frontier import compute_efficient_frontier

# Compute efficient frontier
frontier = compute_efficient_frontier(
    returns_func=portfolio_returns,
    n_assets=2,
    risk_measure=MetricType.STANDARD_DEVIATION,
    n_points=20
)

# Access frontier points
for point in frontier.points:
    print(f"Risk: {point.risk:.4f}, Return: {point.return_:.4f}")
```

## Next Steps

- Learn about [different objective types](objectives.md)
- Explore [constraint options](constraints.md)
- See [complete examples](examples.md)
