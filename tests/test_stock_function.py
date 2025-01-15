import pybacktestchain
from pybacktestchain.data_module import get_stocks_data
from package_203_project.stocks_function import StockAnalysis
from package_203_project.stocks_function import StockDataHandler
from package_203_project.stocks_function import BenchmarkHandler
import logging
from package_203_project.stocks_function import run_stock_analysis, get_stocks_user_input


if __name__ == "__main__":
    run_stock_analysis()