
import pandas as pd
import logging
from dataclasses import dataclass
from datetime import datetime
import plotly.graph_objects as go
import os 
import pickle
from pybacktestchain.data_module import UNIVERSE_SEC, FirstTwoMoments, get_stocks_data, DataModule, Information
from pybacktestchain.utils import generate_random_name
from pybacktestchain.blockchain import Block, Blockchain
from numba import jit 
from datetime import timedelta, datetime
from pybacktestchain.broker import EndOfMonth, StopLoss, Broker
import plotly.graph_objects as go
from scipy.stats import kurtosis, skew
import matplotlib.pyplot as plt


# -----------------------------------------------------------
# Increase the frequency of the rebalancing 
# -----------------------------------------------------------


@dataclass
class RebalanceFlag:
    def time_to_rebalance(self, t: datetime):
        pass 

@dataclass
class EndOfMonth(RebalanceFlag):
    def time_to_rebalance(self, t: datetime):
        # Convert to pandas Timestamp for convenience
        pd_date = pd.Timestamp(t)
        # Get the last business day of the month
        last_business_day = pd_date + pd.offsets.BMonthEnd(0)
        # Check if the given date matches the last business day
        return pd_date == last_business_day

class EndOfWeek(RebalanceFlag):
    def time_to_rebalance(self, t: datetime):
        # Convert to pandas Timestamp for convenience
        pd_date = pd.Timestamp(t)
        # Check if the current day is the last business day of the week
        return pd_date.weekday() == 4

class EndOfDay(RebalanceFlag):
    def time_to_rebalance(self, t: datetime):
        # Always true as we need to rebalance everyday
        return True


# -----------------------------------------------------------
# Modified Backtest function. 
# Save the Backtest portfolio values to a DataFrame and returns analysis: returns, volatility, skew, kurtosis.
# Plot the Portfolio values (cumulated returns, weight allocation through time)
# -----------------------------------------------------------


@dataclass
class Backtest:
    initial_date: datetime
    final_date: datetime
    universe = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'INTC', 'CSCO', 'NFLX']
    information_class: type = Information
    s: timedelta = timedelta(days=360)
    time_column: str = 'Date'
    company_column: str = 'ticker'
    adj_close_column: str = 'Adj Close'
    rebalance_flag: type = EndOfMonth # Default rebalancing is monthly
    risk_model: type = StopLoss
    initial_cash: int = 1000000  # Initial cash in the portfolio
    name_blockchain: str = 'backtest'
    verbose: bool = True
    broker = Broker(cash=initial_cash, verbose=verbose)

    def __post_init__(self):
        self.backtest_name = generate_random_name()
        self.broker.initialize_blockchain(self.name_blockchain)
        # **Moved rebalance flag validation inside __post_init__**
        rebalance_map = {
            "daily": EndOfDay,         
            "weekly": EndOfWeek,      
            "monthly": EndOfMonth     
        }
        if isinstance(self.rebalance_flag, str):
            if self.rebalance_flag not in rebalance_map:
                raise ValueError("Invalid rebalance frequency. Choose from 'daily', 'weekly', or 'monthly'.")
            self.rebalance_flag = rebalance_map[self.rebalance_flag]  # Map string to class
        


    def run_backtest(self):
        logging.info(f"Running backtest from {self.initial_date} to {self.final_date}.")
        logging.info(f"Retrieving price data for universe.")
        self.risk_model = self.risk_model(threshold=0.1)

        # Convert initial and final dates to string
        init_ = self.initial_date.strftime('%Y-%m-%d')
        final_ = self.final_date.strftime('%Y-%m-%d')

        df = get_stocks_data(self.universe, init_, final_)
        data_module = DataModule(df)

        info = self.information_class(
            s=self.s,
            data_module=data_module,
            time_column=self.time_column,
            company_column=self.company_column,
            adj_close_column=self.adj_close_column,
        )

        # Initialize a DataFrame to store portfolio values
        portfolio_values = []

        # Run the backtest
        for t in pd.date_range(start=self.initial_date, end=self.final_date, freq='D'):
            if self.risk_model is not None:
                portfolio = info.compute_portfolio(t, info.compute_information(t))
                prices = info.get_prices(t)
                self.risk_model.trigger_stop_loss(t, portfolio, prices, self.broker)

            if self.rebalance_flag().time_to_rebalance(t):
                logging.info("-----------------------------------")
                logging.info(f"Rebalancing portfolio at {t}")
                information_set = info.compute_information(t)
                portfolio = info.compute_portfolio(t, information_set)
                prices = info.get_prices(t)
                self.broker.execute_portfolio(portfolio, prices, t)

            # Calculate and store portfolio value for the day
            prices = info.get_prices(t)
            if prices:
                portfolio_value = self.broker.get_portfolio_value(prices)
                portfolio_values.append({'Date': t, 'PortfolioValue': portfolio_value})

        # Save the portfolio values to a DataFrame
        portfolio_values_df = pd.DataFrame(portfolio_values)

        # Calculate portfolio returns and add them as a new column
        portfolio_values_df['PortfolioReturn'] = portfolio_values_df['PortfolioValue'].pct_change()
        # Calculate cumulative returns
        portfolio_values_df['CumulativeReturn'] = (1 + portfolio_values_df['PortfolioReturn']).cumprod() - 1

        # Print the DataFrame directly
        print(portfolio_values_df)
        
        # Calculate and print statistics
        if 'PortfolioReturn' in portfolio_values_df.columns:
            valid_returns = portfolio_values_df['PortfolioReturn'].dropna()
            avg_return = valid_returns.mean()
            std_dev = valid_returns.std()
            kurt = kurtosis(valid_returns, fisher=True)
            skewness = skew(valid_returns)

            print("Portfolio Return Statistics:")
            print(f"Average Return: {avg_return:.6f}")
            print(f"Standard Deviation: {std_dev:.6f}")
            print(f"Excess Kurtosis: {kurt:.6f}")
            print(f"Skewness: {skewness:.6f}")

            # Normal VaR if skewness and kurtosis are between -1 and 1 - because we considere it is enough to consider it normally distributed 
            if -1 <= skewness <= 1 and -1 <= kurt <= 1:
                z_alpha = 1.645  # For 95% confidence level
                VaR_normal = -(avg_return - z_alpha * std_dev) * self.initial_cash
                print(f"Normal VaR (95% Confidence): {VaR_normal:.6f}")
            else:
                # Adjusted VaR formula with skewness and kurtosis (Cornish-Fisher Expansion)
                z_alpha = 1.645  # For 95% confidence level
                VaR_adjusted = -(avg_return - (z_alpha * std_dev + (1 / 6) * (z_alpha**2 - 1) * skewness + (1 / 24) * (z_alpha**3 - 3 * z_alpha) * kurt)) * self.initial_cash 
                print(f"Adjusted VaR (95% Confidence): {VaR_adjusted:.6f}")

        # Create backtests folder if it does not exist
        if not os.path.exists('backtests_portfolio_values'):
            os.makedirs('backtests_portfolio_values')

        # Save the DataFrame to a CSV file
        portfolio_values_df.to_csv(f"backtests_portfolio_values/{self.backtest_name}_portfolio_values.csv", index=False)

        logging.info(f"Backtest completed. Final portfolio value: {self.broker.get_portfolio_value(info.get_prices(self.final_date))}")
        df = self.broker.get_transaction_log()

        # Create backtests folder if it does not exist
        if not os.path.exists('backtests'):
            os.makedirs('backtests')

        # Save transaction log to CSV
        df.to_csv(f"backtests/{self.backtest_name}.csv")

        # Store the backtest in the blockchain
        self.broker.blockchain.add_block(self.backtest_name, df.to_string())

        # Ensure the folder for graphs exists
        graphs_folder = 'backtests_portfolio_graphs'
        if not os.path.exists(graphs_folder):
            os.makedirs(graphs_folder)

        # Plot portfolio returns
        plt.figure(figsize=(10, 6))
        plt.plot(portfolio_values_df['Date'], portfolio_values_df['CumulativeReturn'], label='Cumulative Return')
        plt.xlabel('Date')
        plt.ylabel('Return')
        plt.title('Portfolio Returns Over Time')
        plt.legend()
        plt.grid(True)

        # Save the graph
        graph_path = os.path.join(graphs_folder, f"{self.backtest_name}_portfolio_returns.png")
        plt.savefig(graph_path)
    

    def plot_portfolio_weights(self, start_date, end_date):
        dates = pd.date_range(start=start_date, end=end_date, freq='M')
        portfolio_weights = []
        stock_list = None

        info = self.information_class(
            s=self.s,
            data_module=DataModule(get_stocks_data(self.universe, '2015-01-01', '2023-01-01')),
            time_column=self.time_column,
            company_column=self.company_column,
            adj_close_column=self.adj_close_column
        )

        for date in dates:
            information_set = info.compute_information(date)
            portfolio = info.compute_portfolio(date, information_set)
            portfolio_weights.append(portfolio)
            if stock_list is None:
                stock_list = list(portfolio.keys())

        df = pd.DataFrame(portfolio_weights, index=dates, columns=stock_list).fillna(0)

        # Create a Plotly figure
        fig = go.Figure()

        # Add a trace for each stock in the portfolio
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

        # Ensure the folder exists
        folder_path = 'plot_portfolio_weight_graphs'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save the figure as a PNG using Plotly's write_image method - better for visualisation of weight allocaton 
        png_path = os.path.join(folder_path, f"{self.backtest_name}_portfolio_weights.png")
        
        # Ensure Kaleido is installed for saving images
        fig.write_image(png_path)

        # Display the figure (optional)
        fig.show()

        print(f"Portfolio weights graph saved as {png_path}")
