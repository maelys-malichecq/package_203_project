import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from typing import List


# Function allowing the user to choose their actions
def user_choose_stocks():
    print("Welcome, you can select your stocks for the backtest")
    print("Here are some popular stokcs :")
    default_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'INTC', 'CSCO', 'NFLX']
    print(", ".join(default_stocks))

    stocks = input("Enter the tickers of the shares you want to include, separated by commas (or press Enter to select all): ")
    if not stocks.strip():
        print("No action specified, use default universe.")
        return default_stocks

    selected_stocks = [stock.strip().upper() for stock in stocks.split(',')]
    print(f"You selected :{', '.join(selected_stocks)}")
    return selected_stocks

# Principal function to execute the program
def main():
    # Choice of stock from the user
    universe = user_choose_stocks()

    # Dates du backtest
    initial_date = datetime(2020, 1, 1)
    final_date = datetime(2021, 1, 1)

    # Backtest
    backtest = Backtest(initial_date=initial_date, final_date=final_date, universe=universe)
    backtest.run()

if __name__ == "__main__":
    main()


def user_choice():
    """User selects parameters for running the backtest."""
      
    while True:
        try:
            initial_cash = int(input("Welcome to the Backtest, please enter your initial cash: "))
            stop_loss_threshold = float(input("Please enter your stop loss threshold in decimal form. For example, if you want to limit your loss to 5%, enter 0.05. A stop loss threshold of 0.1 means you are willing to tolerate a 10% loss before selling. Make sure to choose a threshold that aligns with your risk tolerance."))
            if stop_loss_threshold >= 1:
                print("Invalid choice. Please enter decimal number")
                break

            start_date_str = input("Please enter the start date for the backtest (YYYY-MM-DD):")
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

            end_date_str = input("Please enter the end date for the backtest (YYYY-MM-DD):")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            if end_date <= start_date:
                print("The end date must be after the start date")
                break
            
            return initial_cash, stop_loss_threshold, start_date, end_date
    
        except ValueError:
            print("Invalid input. Investment and threshold has to be numeric values and dates has to be in the format YYY-MM-DD")