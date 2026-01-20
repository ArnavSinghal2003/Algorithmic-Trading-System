import pandas as pd

def moving_average_strategy(data, short_window=20, long_window=50):
    df = data.copy()

    df["Short_MA"] = df["Close"].rolling(window=short_window).mean()
    df["Long_MA"] = df["Close"].rolling(window=long_window).mean()

    df["Signal"] = 0
    df.loc[df["Short_MA"] > df["Long_MA"], "Signal"] = 1
    df.loc[df["Short_MA"] < df["Long_MA"], "Signal"] = -1

    return df
