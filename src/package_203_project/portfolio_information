def return_portfolio(portfolio: dict, information_set):
    """
    To compute the return of a given portfolio.
    """
    expected_returns = information_set.get('expected_returns')  # Un vecteur des rendements attendus pour chaque actif
    weights = np.array(list(portfolio.values()))  # Poids des actifs dans le portefeuille

    # Calculer le rendement du portefeuille
    portfolio_return = np.dot(weights.T, expected_returns)
    return portfolio_return


def vol_portfolio(portfolio: dict, information_set):
        """
        To compute the volatility of a given portfolio.
        """
        Sigma = information_set.get('covariance_matrix')
        weights = np.array(list(portfolio.values()))
        
        # Compute portfolio variance and volatility
        portfolio_variance = np.dot(weights.T, np.dot(Sigma, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        return portfolio_volatility

def volatility_contribution(portfolio: dict, information_set):
    """
    To compute the contribution of each asset to the portfolio's total volatility.
    """
    Sigma = information_set.get('covariance_matrix')  # Matrice de covariance
    weights = np.array(list(portfolio.values()))  # Poids des actifs dans le portefeuille

    # Compute vol contribution
    marginal_volatility = np.dot(Sigma, weights)  # Contribution marginale de chaque actif
    total_portfolio_volatility = np.sqrt(np.dot(weights.T, marginal_volatility))  # Volatilité totale
    contributions = weights * marginal_volatility / total_portfolio_volatility  # Contribution en pourcentage

    return contributions


def skewness_portfolio(portfolio: dict, information_set):
    """
    To compute the skewness of a given portfolio.
    """
    skewness_vector = information_set.get('skewness')  # Skewness pour chaque actif
    weights = np.array(list(portfolio.values()))  # Poids des actifs dans le portefeuille

    # Calculate skewness  
    portfolio_skewness = np.dot(weights.T, skewness_vector)
    return portfolio_skewness

def kurtosis_portfolio(portfolio: dict, information_set):
    """
    To compute the kurtosis of a given portfolio.
    """
    kurtosis_vector = information_set.get('kurtosis')  # Kurtosis pour chaque actif
    weights = np.array(list(portfolio.values()))  # Poids des actifs dans le portefeuille

    # Calculate kurtosis  
    portfolio_kurtosis = np.dot(weights.T, kurtosis_vector)
    return portfolio_kurtosis

def beta_portfolio(portfolio: dict, information_set):
    """
    To compute the beta of a given portfolio relative to the market.
    """
    betas = information_set.get('betas')  # Beta pour chaque actif
    weights = np.array(list(portfolio.values()))  # Poids des actifs dans le portefeuille

    # Calculate beta  
    portfolio_beta = np.dot(weights.T, betas)
    return portfolio_beta
