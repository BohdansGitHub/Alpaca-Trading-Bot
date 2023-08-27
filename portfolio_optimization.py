from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import expected_returns, risk_models, objective_functions


def calculate_optimal_weights(data, risk_free_rate):
    """
    Calculate optimal portfolio weights using mean-variance optimization.

    This function takes historical price data and a risk-free rate as inputs and performs
    mean-variance optimization to determine the optimal weights for a portfolio. The goal is
    to maximize the Sharpe ratio, which balances risk and return.

    Args:
        data (pandas.DataFrame): Historical price data containing columns like 'symbol', 'close', etc.
        risk_free_rate (float): The risk-free rate used in the optimization calculation.

    Returns:
        dict: A dictionary where keys are trading symbols and values are corresponding optimized portfolio weights.
    """
    rfr_annualized = risk_free_rate
    rfr = (1 + rfr_annualized)**(1/360) - 1

    # Calculate historical returns from price data
    returns = data.groupby('symbol')['close'].pct_change().dropna()
    returns = returns.unstack(level=0)  # Pivoting the first level (symbol) to columns

    # Calculate expected returns and covariance matrix
    mu = expected_returns.mean_historical_return(returns, returns_data=True)
    cov = risk_models.sample_cov(returns, returns_data=True)

    # Initialize EfficientFrontier with expected returns and covariance matrix
    ef = EfficientFrontier(mu, cov, weight_bounds=(0, 1))  # Change parameters to (-1, 1) to allow short positions
    ef.add_objective(objective_functions.L2_reg, gamma=1)  # Regularisation to reduce the number of negligible weights

    # Perform mean-variance optimization for maximum Sharpe ratio
    optimal_weights = ef.max_sharpe(risk_free_rate=rfr)

    # Print optimized portfolio weights
    print("Optimized weights:", optimal_weights)

    # Calculate and print optimized portfolio performance
    ef.portfolio_performance(verbose=True)

    return optimal_weights
