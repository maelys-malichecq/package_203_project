
from dataclasses import dataclass
import numpy as np
import logging
import yfinance as yf
import pandas as pd
import statsmodels.api as sm
import numpy as np
import pybacktestchain
from pybacktestchain.data_module import get_stocks_data, get_stock_data
import datetime
import os
import logging
import matplotlib.pyplot as plt

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
        # Align time zones and remove conflicting Date formats
        log_returns_pivot.index = pd.to_datetime(log_returns_pivot.index).tz_localize(None)
        bench_log_returns['Date'] = pd.to_datetime(bench_log_returns['Date']).dt.tz_localize(None)

        # Merge the datasets
        merged_data = log_returns_pivot.merge(
            bench_log_returns.set_index('Date'),
            left_index=True,
            right_index=True,
            how='inner'
        )
        if merged_data.empty:
            raise ValueError("Merged data is empty, ensure overlapping dates btw stocks and benchmark")
        
        # Perform regression for each stock
        bench_return = merged_data['log_return']
        betas = []
        stock_betas = {}

        for stock in log_returns_pivot.columns:
            if merged_data[stock].isna().all():
                stock_beta[stock] = None
                continue

            y = merged_data[stock].dropna()
            X = sm.add_constant(bench_return.loc[y.index])
            model = sm.OLS(y, X, missing='drop').fit()
            beta = model.params[1]
            betas.append(beta)
            stock_betas[stock] = beta

        average_beta = np.mean([b for b in betas if b is not None])  # In order to ignore None values
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
        # Use of the pybacktestchain get_stocks_data function

        stock_data = get_stocks_data(self.tickers, self.start_date, self.end_date)
        
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
        
        # Use of get_stock_data from pybacktestchain
        bench_data = get_stock_data(ticker, self.start_date, self.end_date)
        if bench_data.empty:
            raise ValueError(f"No data found for benchmark '{self.benchmark}'")

        # Ensure the index is reset and Date is a column
        if 'Date' not in bench_data.columns:
            bench_data = bench_data.reset_index()
        
        # Ensure the data is sorted by date
        bench_data.sort_values(by='Date', inplace=True)
        
        # Calculate log returns
        bench_data['log_return'] = np.log(bench_data['Close'] / bench_data['Close'].shift(1))
        
        return bench_data[['Date', 'log_return']].dropna().reset_index(drop=True)


########## USER INTERACTION ##########


# Enable logging
logging.basicConfig(level=logging.INFO)


def get_stocks_user_input():
    """
    Collect user input for stocks, date range, and benchmark.
    """
    tickers = input("Enter stock tickers separated by commas (e.g., AAPL, MSFT, GOOGL): ").split(",")
    tickers = [ticker.strip().upper() for ticker in tickers]  # Clean input

    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

    print("\nAvailable Benchmarks:")
    print("1. SPX (S&P 500)")
    print("2. CAC40 (CAC 40)")
    print("3. EUROSTOXX (Euro Stoxx 50)")
    print("4. MSCI (MSCI Index)")
    benchmark_map = {"1": "SPX", "2": "CAC40", "3": "EUROSTOXX", "4": "MSCI"}
    benchmark_choice = input("Choose a benchmark (1-4): ").strip()

    if benchmark_choice not in benchmark_map:
        raise ValueError("Invalid benchmark choice. Please select a number between 1 and 4.")
    benchmark = benchmark_map[benchmark_choice]

    return tickers, start_date, end_date, benchmark

def run_stock_analysis():

    """
    Function to run the stock analysis with user inputs.
    """

    # Initialize variables to None to handle exceptions gracefully
    log_returns_pivot = None
    bench_log_returns = None
    stock_data = None
    ranked_stocks = None

    try:
        tickers, start_date, end_date, benchmark = get_stocks_user_input()

        # Stock data handler
        print("\n=== Fetching Log Returns Pivot ===")
        stock_handler = StockDataHandler(
            tickers=tickers,
            start_date=start_date,
            end_date=end_date
        )

        log_returns_pivot = stock_handler.get_stocks_log_returns()
        print("\n=== Log Returns Pivot Table (Head) ===")
        print(log_returns_pivot.head().to_string())

        # Benchmark handler
        print("\n=== Fetching Benchmark Log Returns ===")
        benchmark_handler = BenchmarkHandler(
            benchmark=benchmark,
            start_date=start_date,
            end_date=end_date
        )
        bench_log_returns = benchmark_handler.get_bench_log_returns()
        print("\n=== Benchmark Log Returns (Head) ===")
        print(bench_log_returns.head().to_string())

        # Rank stocks by volume
        print("\n=== Fetching Stock Data and Ranking by Volume ===")
        stock_data = get_stocks_data(
            tickers=tickers,
            start_date=start_date,
            end_date=end_date
        )
        
        ranked_stocks = StockAnalysis.rank_stocks_by_volume(stock_data)
        print("\n=== Ranked Stocks by Volume ===")
        print(ranked_stocks.to_string())

        # Calculate average beta
        print("\n=== Calculating Betas ===")
        print("\nLog Returns Pivot Table :") # Print in case I need to debug 
        print(log_returns_pivot.head().to_string())
        print("\nBenchmark Log Returns (Full):")
        print(bench_log_returns.head().to_string())

        beta_result = StockAnalysis.calculate_average_beta(log_returns_pivot, bench_log_returns)
        print("\n=== Betas for Each Stock ===")
        for stock, beta in beta_result["stock_betas"].items():
            print(f"{stock}: {beta:.4f}")
        print(f"\n=== Average Beta ===\n{beta_result['average_beta']:.4f}")

    except Exception as e:
        logging.error("An error occurred during stock analysis:", exc_info=True)

    # Plot graphs if data is available
    if log_returns_pivot is not None and bench_log_returns is not None:

        # Ensure the folder for graphs exists
        graphs_folder = "stocks_function_graphs"
        if not os.path.exists(graphs_folder):
            os.makedirs(graphs_folder)

        # Generate a unique filename using the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        graphs_path = os.path.join(graphs_folder, f"comparison_graph_{timestamp}.png")

        # Create a single document for all three graphs
        plt.figure(figsize=(18, 18))

        # Subplot 1: Cumulative Returns
        cumulative_stock_returns = (log_returns_pivot + 1).cumprod()
        cumulative_bench_returns = (bench_log_returns['log_return'] + 1).cumprod()

        plt.subplot(3, 1, 1)
        for stock in cumulative_stock_returns.columns:
            plt.plot(cumulative_stock_returns.index, cumulative_stock_returns[stock], label=stock)
        plt.plot(bench_log_returns['Date'], cumulative_bench_returns, label=f"Benchmark ({benchmark})", linewidth=2, linestyle="--")
        plt.title("Cumulative Returns Comparison")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Returns")
        plt.legend()
        plt.grid(True)

        # Subplot 2: Rolling Volatility
        rolling_volatility_stocks = log_returns_pivot.rolling(30).std()
        rolling_volatility_bench = bench_log_returns['log_return'].rolling(30).std()

        plt.subplot(3, 1, 2)
        for stock in rolling_volatility_stocks.columns:
            plt.plot(rolling_volatility_stocks.index, rolling_volatility_stocks[stock], label=f"{stock} Volatility")
        plt.plot(bench_log_returns['Date'], rolling_volatility_bench, label="Benchmark Volatility", linewidth=2, linestyle="--")
        plt.title("Rolling Volatility Comparison")
        plt.xlabel("Date")
        plt.ylabel("Volatility")
        plt.legend()
        plt.grid(True)

        # Subplot 3: Sharpe Ratio Comparison
        mean_returns_stocks = log_returns_pivot.mean()
        std_returns_stocks = log_returns_pivot.std()
        sharpe_ratios_stocks = mean_returns_stocks / std_returns_stocks

        mean_returns_bench = bench_log_returns['log_return'].mean()
        std_returns_bench = bench_log_returns['log_return'].std()
        sharpe_ratio_bench = mean_returns_bench / std_returns_bench

        plt.subplot(3, 1, 3)
        plt.bar(sharpe_ratios_stocks.index, sharpe_ratios_stocks, label="Stocks")
        plt.axhline(sharpe_ratio_bench, color='red', linestyle='--', linewidth=2, label="Benchmark Sharpe Ratio")
        plt.title("Sharpe Ratio Comparison")
        plt.xlabel("Stocks")
        plt.ylabel("Sharpe Ratio")
        plt.legend()
        plt.grid(True)

        # Save the combined figure
        plt.tight_layout()
        plt.savefig(graphs_path)
        plt.show()

        print(f"Graphs saved in: {graphs_path}")

    else:
        print("Graphs could not be generated due to missing data.")

