def configure_and_run_backtest():
    import datetime
    import pandas as pd
    from pybacktestchain.broker import StopLoss
    from pybacktestchain.data_module import FirstTwoMoments
    from package_203_project.modified_portfolio_methods import SharpeRatioMaximization, EqualWeightPortfolio
    from package_203_project.modified_broker import Backtest

    print("Configure your backtest parameters:")

    # User input for initial and final dates
    initial_date = input("Enter the initial date (YYYY-MM-DD): ")
    final_date = input("Enter the final date (YYYY-MM-DD): ")

    try:
        initial_date = datetime.datetime.strptime(initial_date, '%Y-%m-%d')
        final_date = datetime.datetime.strptime(final_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # User input for the universe of stocks
    universe_options = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'INTC', 'CSCO', 'NFLX']
    print(f"Available stocks: {', '.join(universe_options)}")
    print("Type 'all' to select all stocks or provide a comma-separated list of tickers.")
    universe_input = input("Enter your universe of stocks: ").strip()

    if universe_input.lower() == 'all':
        universe = universe_options
    else:
        universe = [ticker.strip().upper() for ticker in universe_input.split(',') if ticker.strip().upper() in universe_options]
        if not universe:
            print("No valid tickers selected. Aborting.")
            return

    # User input for rebalancing frequency
    print("Rebalancing options: daily, weekly, monthly")
    rebalance_input = input("Enter rebalancing frequency: ").strip().lower()

    if rebalance_input not in ['daily', 'weekly', 'monthly']:
        print("Invalid rebalancing frequency. Choose from 'daily', 'weekly', or 'monthly'.")
        return

    # User input for initial cash
    try:
        initial_cash = int(input("Enter the initial cash amount (integer): ").strip())
    except ValueError:
        print("Invalid cash amount. Please enter an integer.")
        return

    # User input for information class
    print("Choose an information class:")
    print("1: SharpeRatioMaximization")
    print("2: EqualWeightPortfolio")
    print("3: FirstTwoMoments")
    information_class_choice = input("Enter 1, 2, or 3: ").strip()

    if information_class_choice == '1':
        information_class = SharpeRatioMaximization
    elif information_class_choice == '2':
        information_class = EqualWeightPortfolio
    elif information_class_choice == '3':
        information_class = FirstTwoMoments
    else:
        print("Invalid choice. Enter 1 for SharpeRatioMaximization, 2 for EqualWeightPortfolio, or 3 for FirstTwoMoments.")
        return

    # Run the backtest
    backtest = Backtest(
        initial_date=initial_date,
        final_date=final_date,
        rebalance_flag=rebalance_input,
        initial_cash=initial_cash,
        information_class=information_class,
        risk_model=StopLoss,
    )

    # Manually set the universe if didn't work 
    backtest.universe = universe

    # Execute the backtest
    backtest.run_backtest()

    # Plot portfolio weights for the same period as the backtest
    backtest.plot_portfolio_weights(initial_date, final_date)




