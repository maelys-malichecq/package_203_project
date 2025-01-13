def rank_stocks_by_volume(df):
    """
    Ranks stocks based on their average trading volume in increasing order. Can be useful if we want to build a liquid portfolio. 

    Args:
        df (pd.DataFrame): The dataframe containing stock data with a 'Volume' column.

    Returns:
        pd.DataFrame: A dataframe with tickers and their average volumes, ranked in increasing order.
    """
    # Calculate the average volume for each stock
    average_volumes = df.groupby('ticker')['Volume'].mean().reset_index()
    
    # Rename the column for clarity
    average_volumes.rename(columns={'Volume': 'average_volume'}, inplace=True)
    
    # Sort by average volume in increasing order
    ranked_stocks = average_volumes.sort_values(by='average_volume', ascending=True).reset_index(drop=True)
    
    return ranked_stocks


def get_stocks_log_returns(tickers, start_date, end_date):
    """
    Retrieves historical data for multiple stocks, calculates their daily log returns,
    and returns a dataframe with dates as rows and tickers as columns.

    Args:
        tickers (list): List of stock tickers.
        start_date (str): Start date in the format 'YYYY-MM-DD'.
        end_date (str): End date in the format 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: A dataframe with dates as rows, tickers as columns, and log returns as values.
    """
    # Get stock data using the existing get_stocks_data function
    stock_data = get_stocks_data(tickers, start_date, end_date)
    
    # Ensure data is sorted by ticker and date
    stock_data.sort_values(by=['ticker', 'Date'], inplace=True)
    
    # Calculate daily log returns for each stock
    stock_data['log_return'] = stock_data.groupby('ticker')['Close'].transform(lambda x: np.log(x / x.shift(1)))
    
    # Pivot the data so that dates are rows and tickers are columns
    pivoted_data = stock_data.pivot(index='Date', columns='ticker', values='log_return')
    
    return pivoted_data
