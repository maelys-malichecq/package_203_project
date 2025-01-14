from dataclasses import dataclass
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pybacktestchain
from pybacktestchain.data_module import DataModule, Information, get_stocks_data
from pybacktestchain.data_module import FirstTwoMoments 
from src.modified_broker import Backtest 
import pandas as pd
from scipy.stats import kurtosis, skew


"This class is responsible for visualizing the evolution of the backtested portfolio weights over the selected period."
"It generates a stacked area chart using Plotly to show the changes in stock weights over time. See test. "

# Initialize the Backtest class with parameters
backtest = Backtest(
    initial_date=datetime(2010, 1, 1),
    final_date=datetime(2021, 1, 1),
    information_class=FirstTwoMoments,
    rebalance_flag=EndOfMonth,
    risk_model=StopLoss,
    initial_cash=1000000,
    name_blockchain='backtest',
    verbose=True
)

# Define a function to print the portfolio
def print_portfolio(backtest, date):
    # Retrieve the information set and portfolio
    info = backtest.information_class(
        s=backtest.s,
        data_module=DataModule(get_stocks_data(backtest.universe, '2015-01-01', '2023-01-01')),
        time_column=backtest.time_column,
        company_column=backtest.company_column,
        adj_close_column=backtest.adj_close_column
    )

    information_set = info.compute_information(date)
    portfolio = info.compute_portfolio(date, information_set)

    # Print the portfolio
    print(f"Portfolio on {date}:")
    for ticker, weight in portfolio.items():
        print(f"{ticker}: {weight:.2%}")

# Function to plot portfolio weights over time
def plot_portfolio_weights(backtest, start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    portfolio_weights = []
    stock_list = None

    info = backtest.information_class(
        s=backtest.s,
        data_module=DataModule(get_stocks_data(backtest.universe, '2015-01-01', '2023-01-01')),
        time_column=backtest.time_column,
        company_column=backtest.company_column,
        adj_close_column=backtest.adj_close_column
    )

    for date in dates:
        information_set = info.compute_information(date)
        portfolio = info.compute_portfolio(date, information_set)
        portfolio_weights.append(portfolio)
        if stock_list is None:
            stock_list = list(portfolio.keys())

    df = pd.DataFrame(portfolio_weights, index=dates, columns=stock_list).fillna(0)

    import plotly.graph_objects as go
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

