import pybacktestchain
from pybacktestchain.data_module import get_stocks_data
from package_203_project.stocks_function import StockAnalysis
from package_203_project.stocks_function import StockDataHandler
from package_203_project.stocks_function import BenchmarkHandler
import logging

# Test code
if __name__ == "__main__":
    
    try:
        # Stock data handler
        stock_handler = StockDataHandler(
            tickers=["SAN", "MC"],
            start_date="2022-01-01",
            end_date="2024-12-31"
        )
        log_returns_pivot = stock_handler.get_stocks_log_returns()
        print("Log Returns Pivot:")
        print(log_returns_pivot.head())

        # Benchmark handler
        benchmark_handler = BenchmarkHandler(
            benchmark="CAC40",
            start_date="2022-01-01",
            end_date="2024-12-31"
        )
        bench_log_returns = benchmark_handler.get_bench_log_returns()
        print("\nBenchmark Log Returns:")
        print(bench_log_returns.head())

        # Rank stocks by volume
        stock_data = get_stocks_data(
            tickers=["SAN", "MC"],
            start_date="2022-01-01",
            end_date="2024-12-31"
        )
        ranked_stocks = StockAnalysis.rank_stocks_by_volume(stock_data)
        print("\nRanked Stocks by Volume:")
        print(ranked_stocks)

        # Calculate average beta
        print(log_returns_pivot)
        print(bench_log_returns)
        beta_result = StockAnalysis.calculate_average_beta(log_returns_pivot, bench_log_returns)
        print("\nBetas for Each Stock:", beta_result["stock_betas"])
        print("Average Beta:", beta_result["average_beta"])

    except Exception as e:
        logging.error("An error occurred during testing", exc_info=True)
