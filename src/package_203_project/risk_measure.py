def max_drawdown_portfolio(portfolio: dict, information_set):
    """
    To compute the maximum drawdown of a given portfolio. 
    """
    portfolio_returns = return_portfolio(portfolio, information_set)
    cumulative_returns = np.cumprod(1 + portfolio_returns)

    # Find the rolling maximum of the cumulative returns
    rolling_max = np.maximum.accumulate(cumulative_returns)
    drawdowns = (cumulative_returns - rolling_max) / rolling_max
    max_drawdown = np.min(drawdowns)
    
    return max_drawdown


def sharpe_ratio_portfolio(portfolio: dict, information_set):
    """
    To compute the Sharpe Ratio of a given portfolio. If returns fail the normality test,
    the function computes the parametric VaR of Galeano instead.
    """
    # Use skewness_portfolio and kurtosis_portfolio to test for normality
    portfolio_skewness = skewness_portfolio(portfolio, information_set)
    portfolio_kurtosis = kurtosis_portfolio(portfolio, information_set)

    # Define thresholds for normality (e.g., skewness close to 0 and kurtosis close to 0)
    if abs(portfolio_skewness) > 0.5 or abs(portfolio_kurtosis) > 1.0:
        # If returns are not normal, compute parametric VaR (Galeano method)
        portfolio_returns = return_portfolio(portfolio, information_set)  # Portfolio returns
        portfolio_mean = np.mean(portfolio_returns)
        portfolio_std = np.std(portfolio_returns)
        confidence_level = 0.95  # Adjust as needed
        
        # Galeano's parametric VaR formula
        var_galeano = portfolio_mean - portfolio_std * np.sqrt(2) * np.log(1 / (1 - confidence_level))
        return {
            "result": "VaR_Galeano",
            "value": var_galeano,
            "skewness": portfolio_skewness,
            "kurtosis": portfolio_kurtosis
        }

    # If returns are normal, calculate Sharpe Ratio
    expected_returns = information_set.get('expected_returns')  # Expected returns for each asset
    risk_free_rate = information_set.get('risk_free_rate', 0)  # Risk-free rate (default to 0 if not provided)
    Sigma = information_set.get('covariance_matrix')  # Covariance matrix
    weights = np.array(list(portfolio.values()))  # Portfolio weights

    # Calculate portfolio return and volatility
    portfolio_return = np.dot(weights.T, expected_returns)
    portfolio_variance = np.dot(weights.T, np.dot(Sigma, weights))
    portfolio_volatility = np.sqrt(portfolio_variance)

    # Compute Sharpe Ratio
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility

    return {
        "result": "Sharpe_Ratio",
        "value": sharpe_ratio,
        "skewness": portfolio_skewness,
        "kurtosis": portfolio_kurtosis
    }
