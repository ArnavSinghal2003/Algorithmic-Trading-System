import streamlit as st
import pandas as pd
from data.data_loader import load_data
from strategies.moving_average import moving_average_strategy
from strategies.rsi import rsi_strategy
from strategies.momentum import momentum_strategy
from backtesting.backtester import backtest
from visuals.plot_ma_strategy import plot_ma_strategy
from visuals.plot_rsi_strategy import plot_rsi_strategy
from visuals.plot_momentum_strategy import plot_momentum_strategy
from visuals.plot_equity import plot_equity_curve

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """Calculate annualized Sharpe ratio"""
    if len(returns) < 2:
        return 0
    excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
    if excess_returns.std() == 0:
        return 0
    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)

def optimize_strategy(strategy_name, data, initial_capital, commission):
    """Optimize strategy parameters using grid search"""
    best_sharpe = -np.inf
    best_params = {}
    
    if strategy_name == "Moving Average Crossover":
        for short in range(5, 51, 5):
            for long in range(short+5, 101, 10):
                strategy_data = moving_average_strategy(data, short_window=short, long_window=long)
                results = backtest(strategy_data, initial_capital, commission)
                returns = results["Strategy_Returns"].dropna()
                sharpe = calculate_sharpe_ratio(returns)
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_params = {"short_window": short, "long_window": long}
                    
    elif strategy_name == "RSI Strategy":
        for period in range(5, 51, 5):
            for ob in range(65, 91, 5):
                for os in range(10, 36, 5):
                    strategy_data = rsi_strategy(data, rsi_period=period, overbought=ob, oversold=os)
                    results = backtest(strategy_data, initial_capital, commission)
                    returns = results["Strategy_Returns"].dropna()
                    sharpe = calculate_sharpe_ratio(returns)
                    if sharpe > best_sharpe:
                        best_sharpe = sharpe
                        best_params = {"rsi_period": period, "overbought": ob, "oversold": os}
                        
    elif strategy_name == "Momentum Strategy":
        for lookback in range(5, 101, 10):
            for thresh in np.arange(-0.05, 0.06, 0.01):
                strategy_data = momentum_strategy(data, lookback_period=lookback, threshold=thresh)
                results = backtest(strategy_data, initial_capital, commission)
                returns = results["Strategy_Returns"].dropna()
                sharpe = calculate_sharpe_ratio(returns)
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_params = {"lookback_period": lookback, "threshold": thresh}
    
    return best_params, best_sharpe

import numpy as np
from scipy import stats

# Top stocks list
TOP_STOCKS = [
    "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NVDA", "META", "NFLX", 
    "BABA", "ORCL", "CRM", "AMD", "INTC", "CSCO", "ADBE", "PYPL", 
    "UBER", "SPOT", "SHOP", "SQ", "Other"
]

st.set_page_config(page_title="Algorithmic Trading Dashboard", layout="wide")

st.title("🚀 Algorithmic Trading Platform Dashboard")

st.markdown("""
Welcome to your interactive trading dashboard! Select parameters, run backtests, and visualize results.
""")

# Sidebar for inputs
st.sidebar.header("📊 Configuration")

symbol = st.sidebar.selectbox("Stock Symbol", TOP_STOCKS, index=TOP_STOCKS.index("AAPL"), help="Select a popular stock or choose 'Other' for custom")

if symbol == "Other":
    symbol = st.sidebar.text_input("Custom Stock Symbol", help="Enter a stock ticker symbol (e.g., AAPL, GOOGL)")

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
with col2:
    end_date = st.date_input("End Date", value=pd.to_datetime("2024-01-01"))

strategy = st.sidebar.selectbox("Trading Strategy", ["Moving Average Crossover", "RSI Strategy", "Momentum Strategy"])

# Strategy parameters
st.sidebar.subheader("Strategy Parameters")

if strategy == "Moving Average Crossover":
    short_window = st.sidebar.slider("Short MA Window", 5, 50, 20, help="Short-term moving average period")
    long_window = st.sidebar.slider("Long MA Window", 20, 200, 50, help="Long-term moving average period")
elif strategy == "RSI Strategy":
    rsi_period = st.sidebar.slider("RSI Period", 5, 50, 14, help="Period for RSI calculation")
    oversold = st.sidebar.slider("Oversold Level", 10, 40, 30, help="RSI level to buy")
    overbought = st.sidebar.slider("Overbought Level", 60, 90, 70, help="RSI level to sell")
elif strategy == "Momentum Strategy":
    lookback_period = st.sidebar.slider("Lookback Period", 5, 100, 20, help="Period to calculate momentum")
    threshold = st.sidebar.slider("Momentum Threshold", -0.1, 0.1, 0.0, step=0.01, help="Threshold for buy/sell signals")

initial_capital = st.sidebar.number_input("Initial Capital ($)", 10000, 1000000, 100000, step=10000)

commission = st.sidebar.slider("Transaction Commission (%)", 0.0, 1.0, 0.1, step=0.01, help="Commission per trade as percentage") / 100

# Run button
if st.sidebar.button("🚀 Run Backtest", type="primary"):
    with st.spinner("Loading data and running backtest..."):
        try:
            # Load data
            data = load_data(symbol, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            
            if data.empty:
                st.error("No data found for the selected symbol and date range.")
                st.stop()
            
            # Apply strategy
            if strategy == "Moving Average Crossover":
                strategy_data = moving_average_strategy(data, short_window=short_window, long_window=long_window)
                plot_func = plot_ma_strategy
            elif strategy == "RSI Strategy":
                strategy_data = rsi_strategy(data, rsi_period=rsi_period, overbought=overbought, oversold=oversold)
                plot_func = plot_rsi_strategy
            elif strategy == "Momentum Strategy":
                strategy_data = momentum_strategy(data, lookback_period=lookback_period, threshold=threshold)
                plot_func = plot_momentum_strategy
            
            # Backtest
            results = backtest(strategy_data, initial_capital=initial_capital, commission=commission)
            
            # Store in session state for persistence
            st.session_state['strategy_data'] = strategy_data
            st.session_state['results'] = results
            st.session_state['plot_func'] = plot_func
            st.session_state['data'] = data
            st.session_state['strategy'] = strategy
            st.session_state['initial_capital'] = initial_capital
            st.session_state['commission'] = commission
            
            st.success("Backtest completed successfully!")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.stop()

# Display results if available
if 'results' in st.session_state:
    results = st.session_state['results']
    strategy_data = st.session_state['strategy_data']
    plot_func = st.session_state['plot_func']
    
    # Metrics
    st.header("📈 Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    final_portfolio = results["Portfolio"].iloc[-1]
    initial_portfolio = results["Portfolio"].iloc[0]
    total_return = (final_portfolio - initial_portfolio) / initial_portfolio * 100
    
    # Calculate Sharpe ratio (simplified)
    returns = results["Strategy_Returns"].dropna()
    if len(returns) > 0:
        sharpe_ratio = returns.mean() / returns.std() * (252 ** 0.5) if returns.std() > 0 else 0
    else:
        sharpe_ratio = 0
    
    # Additional metrics
    portfolio_values = results["Portfolio"]
    
    # Maximum Drawdown
    peak = portfolio_values.expanding().max()
    drawdown = (portfolio_values - peak) / peak
    max_drawdown = drawdown.min() * 100  # Convert to percentage
    
    # Win Rate and Profit Factor
    trades = strategy_data["Signal"].diff().fillna(0)
    trade_signals = trades[trades != 0]
    if len(trade_signals) > 0:
        # Calculate returns per trade (simplified)
        trade_returns = []
        entry_price = None
        for idx, signal in trade_signals.items():
            if signal == 1 and entry_price is None:  # Buy
                entry_price = float(strategy_data.loc[idx, "Close"])
            elif signal == -1 and entry_price is not None:  # Sell
                exit_price = float(strategy_data.loc[idx, "Close"])
                trade_return = (exit_price - entry_price) / entry_price
                trade_returns.append(trade_return)
                entry_price = None
        
        if trade_returns:
            winning_trades = [r for r in trade_returns if r > 0]
            losing_trades = [r for r in trade_returns if r < 0]
            win_rate = len(winning_trades) / len(trade_returns) * 100
            gross_profit = sum(winning_trades)
            gross_loss = abs(sum(losing_trades))
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
            total_trades = len(trade_returns)
        else:
            win_rate = 0
            profit_factor = 0
            total_trades = 0
    else:
        win_rate = 0
        profit_factor = 0
        total_trades = 0
    
    # Calmar Ratio
    calmar_ratio = total_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    # Sortino Ratio (downside deviation)
    downside_returns = returns[returns < 0]
    if len(downside_returns) > 0:
        sortino_ratio = returns.mean() / downside_returns.std() * (252 ** 0.5) if downside_returns.std() > 0 else 0
    else:
        sortino_ratio = 0
    
    with col1:
        st.metric("Final Portfolio Value", f"${final_portfolio:,.2f}")
    with col2:
        st.metric("Total Return", f"{total_return:.2f}%")
    with col3:
        st.metric("Max Drawdown", f"{max_drawdown:.2f}%")
    with col4:
        st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
    
    # Additional metrics in second row
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    with col6:
        st.metric("Profit Factor", f"{profit_factor:.2f}")
    with col7:
        st.metric("Calmar Ratio", f"{calmar_ratio:.2f}")
    with col8:
        st.metric("Sortino Ratio", f"{sortino_ratio:.2f}")
    
    # Trade statistics
    st.subheader("Trade Statistics")
    col9, col10 = st.columns(2)
    with col9:
        st.metric("Total Trades", total_trades)
    with col10:
        st.metric("Avg Annual Return", f"{total_return * 252 / len(results):.2f}%")  # Rough estimate
    st.header("📊 Charts")
    tab1, tab2 = st.tabs(["Strategy Signals", "Equity Curve"])
    
    with tab1:
        fig1 = plot_func(strategy_data)
        st.pyplot(fig1)
    
    with tab2:
        fig2 = plot_equity_curve(results)
        st.pyplot(fig2)
    
    # Data tables
    st.header("📋 Data")
    with st.expander("Strategy Data"):
        st.dataframe(strategy_data.tail(20))
    
    with st.expander("Backtest Results"):
        st.dataframe(results.tail(20))

else:
    st.info("Configure parameters in the sidebar and click 'Run Backtest' to get started.")

# Optimization section
if 'results' in st.session_state:
    st.header("⚡ Parameter Optimization")
    st.markdown("Optimize strategy parameters to maximize Sharpe ratio using grid search.")
    
    if st.button("🚀 Optimize Parameters", type="secondary"):
        with st.spinner("Optimizing parameters... This may take a moment."):
            try:
                data = st.session_state['data']  # Need to store data
                strategy = st.session_state['strategy']
                initial_capital = st.session_state['initial_capital']
                commission = st.session_state['commission']
                
                best_params, best_sharpe = optimize_strategy(strategy, data, initial_capital, commission)
                
                st.success(f"Optimization complete! Best Sharpe Ratio: {best_sharpe:.2f}")
                st.subheader("Optimal Parameters:")
                for param, value in best_params.items():
                    st.write(f"**{param.replace('_', ' ').title()}:** {value}")
                    
                # Store optimal params
                st.session_state['optimal_params'] = best_params
                
            except Exception as e:
                st.error(f"Optimization failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")