from data.data_loader import load_data
from strategies.moving_average import moving_average_strategy
from strategies.rsi import rsi_strategy
from backtesting.backtester import backtest
from visuals.plot_ma_strategy import plot_ma_strategy
from visuals.plot_rsi_strategy import plot_rsi_strategy
from visuals.plot_equity import plot_equity_curve

# Load data
data = load_data("AAPL", "2020-01-01", "2024-01-01")

# Apply MA strategy
print("Running Moving Average Strategy...")
ma_strategy_data = moving_average_strategy(data)
ma_results = backtest(ma_strategy_data, commission=0.0)
plot_ma_strategy(ma_strategy_data)
plot_equity_curve(ma_results, "ma_equity_curve.png")
print("MA Strategy plots saved.")

# Apply RSI strategy
print("Running RSI Strategy...")
rsi_strategy_data = rsi_strategy(data)
rsi_results = backtest(rsi_strategy_data, commission=0.0)
plot_rsi_strategy(rsi_strategy_data)
plot_equity_curve(rsi_results, "rsi_equity_curve.png")
print("RSI Strategy plots saved.")

print("All plots saved successfully in images/ folder")
