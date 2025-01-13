
    def plot_results(self, broker):
        df = broker.get_portfolio_values()
        df.set_index('Date', inplace=True)

        # Forcing conversion into numerical data
        df['Portfolio Value'] = pd.to_numeric(df['Portfolio Value'], errors='coerce')

        # Delete na
        df.dropna(subset=['Portfolio Value'], inplace=True)

        # Plot data
        df['Portfolio Value'].plot(title='Portfolio Value Over Time', figsize=(10, 6))
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.grid()
        plt.show()