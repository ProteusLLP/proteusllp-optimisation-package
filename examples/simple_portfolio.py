"""Simple two-asset portfolio optimization example.

This example demonstrates:
- Creating PAL stochastic variables
- Defining optimization objectives
- Running basic optimization
- Interpreting results
"""

from pop import (
    ObjectiveSpec,
    OptimizationInput,
    scipy_optimize,
)
from pop.config import MetricType, OptimizationDirection
from pal import StochasticScalar


def main():
    """Run simple portfolio optimization."""
    print("=" * 60)
    print("Simple Portfolio Optimization Example")
    print("=" * 60)

    # Create two assets with different risk-return profiles
    print("\n1. Creating stochastic variables for two assets...")

    # Asset A: Higher return, higher risk
    returns_a = StochasticScalar(mean=0.08, std=0.15, size=10000)
    print(f"   Asset A: Mean={returns_a.mean():.2%}, Std={returns_a.std():.2%}")

    # Asset B: Lower return, lower risk
    returns_b = StochasticScalar(mean=0.06, std=0.10, size=10000)
    print(f"   Asset B: Mean={returns_b.mean():.2%}, Std={returns_b.std():.2%}")

    # Define portfolio returns function
    def portfolio_returns(weights):
        """Calculate portfolio returns given weights."""
        return weights[0] * returns_a + weights[1] * returns_b

    # Define objective: maximize expected return
    print("\n2. Setting up optimization objective...")
    objective = ObjectiveSpec(
        metric_type=MetricType.MEAN,
        direction=OptimizationDirection.MAXIMIZE,
        target_value=None,  # No target, just maximize
    )
    print(f"   Objective: {objective.direction.value} {objective.metric_type.value}")

    # Create optimization input
    print("\n3. Configuring optimization...")
    opt_input = OptimizationInput(
        objectives=[objective],
        n_assets=2,
        initial_weights=[0.5, 0.5],
        box_constraints=[(0.0, 1.0), (0.0, 1.0)],  # Weights between 0 and 1
    )
    print(f"   Initial weights: {opt_input.initial_weights}")
    print(f"   Box constraints: {opt_input.box_constraints}")

    # Run optimization
    print("\n4. Running optimization...")
    result = scipy_optimize(portfolio_returns, opt_input, method="SLSQP")

    # Display results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    print("\nOptimal weights:")
    print(f"  Asset A: {result.optimal_weights[0]:.2%}")
    print(f"  Asset B: {result.optimal_weights[1]:.2%}")
    print(f"  Sum: {sum(result.optimal_weights):.2%}")

    # Calculate portfolio metrics
    optimal_portfolio = portfolio_returns(result.optimal_weights)
    print("\nPortfolio metrics:")
    print(f"  Expected return: {optimal_portfolio.mean():.2%}")
    print(f"  Standard deviation: {optimal_portfolio.std():.2%}")

    print("\n" + "=" * 60)
    print("Note: Pure return maximization allocates 100% to highest return asset.")
    print("See risk_return_tradeoff.py for efficient frontier examples.")
    print("=" * 60)


if __name__ == "__main__":
    main()
