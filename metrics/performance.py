import numpy as np

def sharpe_ratio(returns, risk_free_rate=0.0):
    return np.mean(returns - risk_free_rate) / np.std(returns)

def max_drawdown(portfolio):
    cumulative_max = portfolio.cummax()
    drawdown = (portfolio - cumulative_max) / cumulative_max
    return drawdown.min()
