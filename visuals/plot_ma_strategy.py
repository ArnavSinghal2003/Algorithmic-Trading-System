import matplotlib.pyplot as plt
import os

def plot_ma_strategy(df):
    # Ensure images folder exists
    os.makedirs("images", exist_ok=True)

    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df["Close"], label="Price", alpha=0.7)
    ax.plot(df["Short_MA"], label="Short MA")
    ax.plot(df["Long_MA"], label="Long MA")

    buy_signals = df[df["Signal"] == 1]
    sell_signals = df[df["Signal"] == -1]

    ax.scatter(buy_signals.index, buy_signals["Close"],
                marker="^", color="green", label="Buy", s=100)
    ax.scatter(sell_signals.index, sell_signals["Close"],
                marker="v", color="red", label="Sell", s=100)

    ax.set_title("Moving Average Crossover Strategy")
    ax.legend()

    # SAVE IMAGE
    plt.savefig("images/ma_strategy.png", bbox_inches="tight")
    return fig
