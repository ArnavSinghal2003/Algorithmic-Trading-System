import yfinance as yf
import pandas as pd

def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data.dropna(inplace=True)
    return data

if __name__ == "__main__":
    df = load_data("AAPL", "2020-01-01", "2024-01-01")
    print(df.head())
