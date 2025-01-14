
import pandas as pd
import logging
from dataclasses import dataclass
from datetime import datetime

import os 
import pickle
from pybacktestchain.data_module import UNIVERSE_SEC, FirstTwoMoments, get_stocks_data, DataModule, Information
from pybacktestchain.utils import generate_random_name
from pybacktestchain.blockchain import Block, Blockchain
from numba import jit 
from datetime import timedelta, datetime
from pybacktestchain.broker import EndOfMonth, StopLoss, Broker


# -----------------------------------------------------------
# Save the Backtest portfolio values to a DataFrame and print it
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
    rebalance_flag: type = EndOfMonth
    risk_model: type = StopLoss
    initial_cash: int = 1000000  # Initial cash in the portfolio
    name_blockchain: str = 'backtest'
    verbose: bool = True
    broker = Broker(cash=initial_cash, verbose=verbose)

    def __post_init__(self):
        self.backtest_name = generate_random_name()
        self.broker.initialize_blockchain(self.name_blockchain)

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

        # Print the DataFrame directly
        print(portfolio_values_df)
        
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
