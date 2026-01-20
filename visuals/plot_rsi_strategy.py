import matplotlib.pyplot as plt
import os

def plot_rsi_strategy(df):
    # Ensure images folder exists
    os.makedirs("images", exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8), sharex=True)

    # Price plot
    ax1.plot(df["Close"], label="Price", alpha=0.7)

    buy_signals = df[df["Signal"] == 1]
    sell_signals = df[df["Signal"] == -1]

    ax1.scatter(buy_signals.index, buy_signals["Close"],
                marker="^", color="green", label="Buy", s=100)
    ax1.scatter(sell_signals.index, sell_signals["Close"],
                marker="v", color="red", label="Sell", s=100)

    ax1.set_title("RSI Strategy")
    ax1.legend()

    # RSI plot
    ax2.plot(df["RSI"], label="RSI", color="blue")
    ax2.axhline(y=70, color="red", linestyle="--", label="Overbought")
    ax2.axhline(y=30, color="green", linestyle="--", label="Oversold")
    ax2.set_ylim(0, 100)
    ax2.legend()

    # SAVE IMAGE
    plt.savefig("images/rsi_strategy.png", bbox_inches="tight")
    return fig