
from pybacktestchain.data_module import get_stocks_data
from package_203_project.stocks_function import rank_stocks_by_volume, get_stocks_log_returns

# Stock data handler
stock_handler = StockDataHandler(
    tickers=["AAPL", "MSFT", "GOOGL"], 
    start_date="2022-01-01", 
    end_date="2022-12-31"
)
log_returns_pivot = stock_handler.get_stocks_log_returns()

# Benchmark handler
benchmark_handler = BenchmarkHandler(
    benchmark="SPX", 
    start_date="2022-01-01", 
    end_date="2022-12-31"
)
bench_log_returns = benchmark_handler.get_bench_log_returns()

print("Log Returns Pivot:")
print(log_returns_pivot.head())

print("\nBenchmark Log Returns:")
print(bench_log_returns.head())


# Rank stocks by volume
stock_data = stock_handler.get_stocks_data()
ranked_stocks = StockAnalysis.rank_stocks_by_volume(stock_data)
print("Ranked Stocks by Volume:")
print(ranked_stocks)

# Calculate average beta
beta_result = StockAnalysis.calculate_average_beta(log_returns_pivot, bench_log_returns)
print("\nBetas for Each Stock:", beta_result["stock_betas"])
print("Average Beta:", beta_result["average_beta"])
