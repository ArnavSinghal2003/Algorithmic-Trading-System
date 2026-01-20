def backtest(data, initial_capital=100000, commission=0.001):
    df = data.copy()
    df["Position"] = df["Signal"].shift()
    df["Returns"] = df["Close"].pct_change()
    df["Strategy_Returns"] = df["Position"] * df["Returns"]

    # Calculate transaction costs
    # df["Position_Change"] = df["Position"].diff().fillna(0)
    # df["Trade"] = df["Position_Change"].abs()  # 1 if position changed
    # df["Costs"] = df["Trade"] * commission * df["Close"]  # Commission cost

    # Adjust returns for costs (approximate)
    # df["Strategy_Returns"] = df["Strategy_Returns"] - (df["Costs"] / initial_capital)

    df["Portfolio"] = (1 + df["Strategy_Returns"]).cumprod() * initial_capital
    return df
