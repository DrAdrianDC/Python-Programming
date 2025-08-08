# Financial Stock Relationship Analysis
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_asset_correlation(tickers, start_date, end_date):
    """
    Fetch historical data for the specified tickers, calculate daily returns,
    and return the correlation matrix.

    Parameters:
        tickers (list): List of asset tickers (e.g., ['AAPL', 'MSFT', 'GOOG']).
        start_date (str): Start date for historical data (e.g., '2022-01-01').
        end_date (str): End date for historical data (e.g., '2023-01-01').

    Returns:
        pd.DataFrame: Correlation matrix of daily returns.
    """
    # Download historical data
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

    # Calculate daily returns
    returns = data.pct_change().dropna()

    # Calculate correlation matrix
    correlation_matrix = returns.corr()

    return correlation_matrix, returns

def plot_correlation_matrix(correlation_matrix, save_path="correlation_heatmap.png"):
    """
    Plot a heatmap of the correlation matrix and save it as a file.

    Parameters:
        correlation_matrix (pd.DataFrame): Correlation matrix to plot.
        save_path (str): Path to save the heatmap image.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
    plt.title('Correlation Matrix of Asset Returns')
    plt.savefig(save_path)
    plt.show()

if __name__ == "__main__":
    # Define the tickers and date range
    tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']
    start_date = '2023-01-01'
    end_date = '2023-12-31'

    # Get the correlation matrix and returns
    correlation_matrix, returns = get_asset_correlation(tickers, start_date, end_date)

    # Print and plot the correlation matrix
    print("Correlation Matrix:")
    print(correlation_matrix)
    plot_correlation_matrix(correlation_matrix, save_path="correlation_heatmap.png")
