
from pybacktestchain.data_module import get_stocks_data
from package_203_project.stocks_function import rank_stocks_by_volume, get_stocks_log_returns

# Get data for multiple stocks
df = get_stocks_data(['AAPL', 'MSFT', 'GOOGL'], '2022-01-01', '2022-12-31')

# Rank stocks based on their average trading volume
ranked_df = rank_stocks_by_volume(df)

print(ranked_df)

tickers = ['AAPL', 'MSFT', 'GOOGL']
start_date = '2022-01-01'
end_date = '2022-12-31'

# Calculer les log returns avec la structure pivotée
log_returns_pivot = get_stocks_log_returns(tickers, start_date, end_date)

print(log_returns_pivot.head())


# Get S&P 500 log returns
spx_log_returns = get_bench_log_returns("2022-01-01", "2022-12-31", benchmark="SPX")
print("SPX Log Returns:")
print(spx_log_returns.head())

# Get CAC 40 log returns
cac40_log_returns = get_bench_log_returns("2022-01-01", "2022-12-31", benchmark="CAC40")
print("\nCAC40 Log Returns:")
print(cac40_log_returns.head())

# Get Euro Stoxx 50 log returns
eurostoxx_log_returns = get_bench_log_returns("2022-01-01", "2022-12-31", benchmark="EUROSTOXX")
print("\nEUROSTOXX Log Returns:")
print(eurostoxx_log_returns.head())

# Get MSCI log returns (if MSCI ticker is valid in your dataset)
msci_log_returns = get_bench_log_returns("2022-01-01", "2022-12-31", benchmark="MSCI")
print("\nMSCI Log Returns:")
print(msci_log_returns.head())


# Example stock log returns pivot table
log_returns_pivot = get_stocks_log_returns_pivot(['AAPL', 'MSFT', 'GOOGL'], '2022-01-01', '2022-12-31')

# Calculate average beta using S&P 500 as benchmark
result_spx = calculate_average_beta(log_returns_pivot, '2022-01-01', '2022-12-31', benchmark="SPX")
print("Betas for each stock with SPX:", result_spx["stock_betas"])
print("Average Beta with SPX:", result_spx["average_beta"])

# Example stock log returns pivot table
log_returns_pivot = get_stocks_log_returns_pivot(['AAPL', 'MSFT', 'GOOGL'], '2022-01-01', '2022-12-31')

# Calculate average beta using CAC40 as benchmark
result_msci = calculate_average_beta(log_returns_pivot, '2022-01-01', '2022-12-31', benchmark="MSCI")
print("\nBetas for each stock with MSCI:", result_msci["stock_betas"])
print("Average Beta with MSCI:", result_msci["average_beta"])