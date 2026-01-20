import pandas as pd

def momentum_strategy(data, lookback_period=20, threshold=0.0):
    """
    Momentum strategy based on price momentum.
    Buys when momentum > threshold, sells when momentum < -threshold.
    Momentum = (current_price - price_lookback) / price_lookback
    """
    df = data.copy()

    # Calculate momentum
    df["Momentum"] = (df["Close"] - df["Close"].shift(lookback_period)) / df["Close"].shift(lookback_period)

    # Generate signals
    df["Signal"] = 0
    df.loc[df["Momentum"] > threshold, "Signal"] = 1
    df.loc[df["Momentum"] < -threshold, "Signal"] = -1

    return df