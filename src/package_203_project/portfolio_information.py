from dataclasses import dataclass
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

import pandas as pd
from scipy.stats import kurtosis, skew

def calculate_statistics(portfolio_values_df: pd.DataFrame) -> dict:
    """
    Calculate average return, standard deviation, kurtosis, and skewness of portfolio returns.

    Parameters:
        portfolio_values_df (pd.DataFrame): DataFrame containing 'PortfolioReturn' column.

    Returns:
        dict: A dictionary containing the calculated statistics.
    """
    if 'PortfolioReturn' not in portfolio_values_df.columns:
        raise ValueError("The DataFrame must contain a 'PortfolioReturn' column.")

    # Filter out NaN values from the PortfolioReturn column
    valid_returns = portfolio_values_df['PortfolioReturn'].dropna()

    # Calculate statistics
    avg_return = valid_returns.mean()
    std_dev = valid_returns.std()
    kurt = kurtosis(valid_returns, fisher=True)
    skewness = skew(valid_returns)

    # Compile results
    stats = {
        "Average Return": avg_return,
        "Standard Deviation": std_dev,
        "Kurtosis": kurt,
        "Skewness": skewness,
    }

    return stats

# Example usage:
# stats = calculate_statistics(portfolio_values_df)
# print(stats)



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