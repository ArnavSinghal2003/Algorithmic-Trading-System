import pandas as pd

def calculate_rsi(data, window=14):
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def rsi_strategy(data, rsi_period=14, overbought=70, oversold=30):
    df = data.copy()
    df["RSI"] = calculate_rsi(df, rsi_period)

    df["Signal"] = 0
    df.loc[df["RSI"] < oversold, "Signal"] = 1
    df.loc[df["RSI"] > overbought, "Signal"] = -1

    return df
