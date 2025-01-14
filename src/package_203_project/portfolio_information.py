from dataclasses import dataclass
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime



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


"This class is responsible for printing the portfolio weights for a specific date."
"It uses the backtest object to retrieve and display portfolio information."

@dataclass
class PortfolioPrinter:
    backtest: any

    def print_portfolio(self, date):
        # Retrieve the information set and portfolio
        info = self.backtest.information_class(
            s=self.backtest.s,
            data_module=DataModule(get_stocks_data(self.backtest.universe, '2015-01-01', '2023-01-01')),
            time_column=self.backtest.time_column,
            company_column=self.backtest.company_column,
            adj_close_column=self.backtest.adj_close_column
        )

        information_set = info.compute_information(date)
        portfolio = info.compute_portfolio(date, information_set)

        # Print the portfolio
        print(f"Portfolio on {date}:")
        for ticker, weight in portfolio.items():
            print(f"{ticker}: {weight:.2%}")


"This class is responsible for visualizing the evolution of portfolio weights over a range of dates."
"It generates a stacked area chart using Plotly to show the changes in stock weights over time."

@dataclass
class PortfolioPlotter:
    backtest: any

    def plot_portfolio_weights(self, start_date, end_date):
        dates = pd.date_range(start=start_date, end=end_date, freq='M')
        portfolio_weights = []
        stock_list = None

        info = self.backtest.information_class(
            s=self.backtest.s,
            data_module=DataModule(get_stocks_data(self.backtest.universe, '2010-01-01', '2025-01-01')),
            time_column=self.backtest.time_column,
            company_column=self.backtest.company_column,
            adj_close_column=self.backtest.adj_close_column
        )

        for date in dates:
            information_set = info.compute_information(date)
            portfolio = info.compute_portfolio(date, information_set)
            portfolio_weights.append(portfolio)
            if stock_list is None:
                stock_list = list(portfolio.keys())

        df = pd.DataFrame(portfolio_weights, index=dates, columns=stock_list).fillna(0)

        fig = go.Figure()

        for stock in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[stock],
                mode='lines',
                stackgroup='one',  # This creates the stacked effect
                name=stock
            ))

        fig.update_layout(
            title='Portfolio Weights Over Time',
            xaxis_title='Date',
            yaxis_title='Portfolio Weights',
            showlegend=True
        )
        fig.show()