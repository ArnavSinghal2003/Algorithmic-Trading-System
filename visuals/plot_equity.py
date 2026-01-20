import matplotlib.pyplot as plt

def plot_equity_curve(df, filename="equity_curve.png"):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df["Portfolio"], label="Portfolio Value")
    ax.set_title("Equity Curve (Backtest Result)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value")
    ax.legend()
    plt.savefig(f"images/{filename}")
    return fig
