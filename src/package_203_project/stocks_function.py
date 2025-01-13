
from dataclasses import dataclass
import numpy as np
import yfinance as yf
import pandas as pd
import statsmodels.api as sm
import numpy as np
import pybacktestchain
from pybacktestchain.data_module import get_stocks_data


@dataclass
class StockAnalysis:
    """
    Performs analysis on stocks, such as ranking by volume and calculating betas.
    """

    @staticmethod
    def rank_stocks_by_volume(df):
        """
        Ranks stocks based on their average trading volume in increasing order.
        """
        average_volumes = df.groupby('ticker')['Volume'].mean().reset_index()
        average_volumes.rename(columns={'Volume': 'average_volume'}, inplace=True)
        ranked_stocks = average_volumes.sort_values(by='average_volume', ascending=True).reset_index(drop=True)
        return ranked_stocks
    
    @staticmethod
    def calculate_average_beta(log_returns_pivot, bench_log_returns):
        """
        Calculates the beta (sensitivity to the chosen benchmark) for each stock and the average beta. 
        Returns a dictionary with betas for each stock and the average beta.
        
        """
        merged_data = log_returns_pivot.merge(
            bench_log_returns, left_index=True, right_on='Date', how='inner'
        ).set_index('Date')
        
        bench_return = merged_data['log_return']
        betas = []
        stock_betas = {}

        for stock in log_returns_pivot.columns:
            y = merged_data[stock]
            X = sm.add_constant(bench_return)
            model = sm.OLS(y, X, missing='drop').fit()
            beta = model.params[1]
            betas.append(beta)
            stock_betas[stock] = beta

        average_beta = np.mean(betas)
        return {"stock_betas": stock_betas, "average_beta": average_beta}

@dataclass
class StockDataHandler:
    """
    Handles fetching and processing stock data.
    """
    tickers: list
    start_date: str
    end_date: str

    def get_stocks_log_returns(self):
        """
        Calculates daily log returns for the stocks.
        """
        stock_data = self.get_stocks_data()
        
        # Ensure the index is reset and Date is a column
        if 'Date' not in stock_data.columns:
            stock_data = stock_data.reset_index()
        
        # Ensure data is sorted by ticker and date
        stock_data.sort_values(by=['ticker', 'Date'], inplace=True)
        
        # Calculate daily log returns for each stock
        stock_data['log_return'] = stock_data.groupby('ticker')['Close'].transform(lambda x: np.log(x / x.shift(1)))
        
        # Pivot the data so that dates are rows and tickers are columns
        pivoted_data = stock_data.pivot(index='Date', columns='ticker', values='log_return')
        return pivoted_data


@dataclass
class BenchmarkHandler:
    """
    Handles fetching and processing benchmark data.
    """
    benchmark: str
    start_date: str
    end_date: str

    benchmark_tickers = {
        "SPX": "^GSPC",  # S&P 500
        "CAC40": "^FCHI",  # CAC 40
        "EUROSTOXX": "^STOXX50E",  # Euro Stoxx 50
        "MSCI": "MSCI"  # MSCI Index (example placeholder)
    }

    def get_bench_log_returns(self):
        """
        Retrieves historical data for the chosen benchmark and calculates log returns.
        """
        if self.benchmark not in self.benchmark_tickers:
            raise ValueError(f"Invalid benchmark. Choose from {list(self.benchmark_tickers.keys())}")
        
        ticker = self.benchmark_tickers[self.benchmark]
        bench_data = yf.Ticker(ticker).history(start=self.start_date, end=self.end_date, auto_adjust=False)
        
        # Ensure the index is reset and Date is a column
        if 'Date' not in bench_data.columns:
            bench_data = bench_data.reset_index()
        
        if bench_data.empty:
            raise ValueError(f"No data found for benchmark '{self.benchmark}'")
        
        # Ensure the data is sorted by date
        bench_data.sort_values(by='Date', inplace=True)
        
        # Calculate log returns
        bench_data['log_return'] = np.log(bench_data['Close'] / bench_data['Close'].shift(1))
        
        return bench_data[['Date', 'log_return']].dropna().reset_index(drop=True)
