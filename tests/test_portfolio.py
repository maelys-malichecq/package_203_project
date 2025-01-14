from datetime import datetime
from package_203_project.modified_broker import Backtest
from package_203_project.modified_portfolio import PortfolioPlotter, plot_portfolio_weights, 


# Example date to display the portfolio
example_date = datetime(2016, 12, 31)
print_portfolio(backtest, example_date)

# Plot portfolio weights from 2016 to 2020
plot_portfolio_weights(backtest, datetime(2016, 1, 1), datetime(2020, 12, 31))
