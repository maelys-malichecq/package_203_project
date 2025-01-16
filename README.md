# package_203_project

A package for doing great things!

## Installation

```bash
$ pip install package_203_project
```

## Usage

- ### **Rebalance Classes**
Three classes define different rebalancing strategies:
1. **`EndOfMonth`**: Rebalances the portfolio on the last business day of each month.
2. **`EndOfWeek`**: Rebalances the portfolio every Friday (last business day of the week).
3. **`EndOfDay`**: Rebalances the portfolio every day.

---
- ### **Portfolio Construction Strategies**
Two classes define different portfolio construction methods:

1. **`SharpeRatioMaximization`**:  
   This class optimizes portfolio weights to maximize the Sharpe ratio.  
   - **Objective**: Maximize the Sharpe ratio by calculating optimal weights based on expected returns and the covariance matrix of asset prices.  

2. **`EqualWeightPortfolio`**:  
   This class assigns equal weights to all assets in the portfolio, providing a simple and robust strategy.  
   - **Objective**: Create a portfolio where each asset has equal weight 1/n, where n is the number of assets.  

---

### **`Backtest` Class**
This is one of the core class of the script, designed to conduct a backtest for a portfolio strategy, modified from the original pybacktestchain script. 

#### **Key Attributes**
- **`initial_date` & `final_date`**: The start and end dates for the backtest.
- **`universe`**: A predefined list of stocks to be included in the portfolio.
- **`rebalance_flag`**: Defines how frequently the portfolio will be rebalanced (daily, weekly, or monthly).
- **`risk_model`**: Implements stop-loss functionality to manage portfolio risk.
- **`broker`**: Handles execution of trades and portfolio transactions.
- **`name_blockchain`**: The blockchain ledger used for storing transaction logs.
- **`information`**: The backtest is run based on a choice on three different portfolio strategies: equal weight pf, max share ratio, or first two moments from pybacktestchain 


### **`run_backtest`**:
   - Retrieves historical stock data for the given time period.
   - Simulates portfolio rebalancing based on the defined frequency.
   - Calculates key portfolio statistics:
     - Returns, volatility, skewness, kurtosis.
     - Value-at-Risk (VaR) either as the normally distributed returns OR an adjusted methods based on skew/kurtosis. 
   - Stores results in CSV files for portfolio values and transaction logs.
   - Saves cumulative returns and transaction details in a blockchain for secure storage.
   - Generates a graph for cumulative returns over time.
   - Visualizes portfolio weight allocation over time.
   - Uses `plotly` for creating interactive, stacked-area graphs of weight allocation = better than matlib for weight allocation vizualisation through time 
   - Saves the resulting graph to a file for analysis.

---

### **Generated Outputs**
1. **CSV Files**:
   - Portfolio values: Saved in `backtests_portfolio_values/`.
   - Transaction logs: Saved in `backtests/`.
2. **Graphs**:
   - Cumulative returns: Saved in `backtests_portfolio_graphs/`.
   - Portfolio weight allocation: Saved in `plot_portfolio_weight_graphs/`.


- ### **Stock Analysis and Benchmarking**
Three classes to handle ndle stock analysis, data management, and benchmark data:

1. **`StockAnalysis`**:  
   Provides key analysis functionalities:  
   - **Rank stocks by volume**: Ranks stocks based on their average trading volume.  
   - **Calculate betas**: Computes the sensitivity (beta) of each stock to a benchmark and calculates the average beta using OLS regression

2. **`StockDataHandler`**:  
   - Draws historical stock data.  
   - Computes daily log returns for each stock and organizes them into a pivot table.  

3. **`BenchmarkHandler`**:  
   - Draws benchmark historical data.  
   - Calculates daily log returns for the chosen benchmark like S&P 500, CAC 40 etc.  
---

### **Interactive User Analysis**
The script allows user interaction to analyze stocks:  
- Users input stock tickers, date range, and benchmark choice.  
- Outputs include:
  - Ranked stocks by volume.
  - Beta values for each stock and the average beta.
  - Visualizations:
    1. **Cumulative Returns**: Comparison of stock and benchmark performance.  
    2. **Rolling Volatility**: Examines stock and benchmark volatility over time.  
    3. **Sharpe Ratios**: Compares risk-adjusted returns for stocks and the benchmark.  

Generated graphs are saved in the `stocks_function_graphs/` folder. 

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`package_203_project` was created by Maelys Malichecq. It is licensed under the terms of the MIT license.

## Credits

`package_203_project` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
