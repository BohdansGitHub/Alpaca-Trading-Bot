def moving_average_crossover_strategy(data, short_window, long_window):
    """
    Apply a moving average crossover strategy to a DataFrame of historical data.

    This function takes historical data as a DataFrame and applies a moving average crossover strategy
    to generate buy/sell signals based on the interaction between short-term and long-term moving averages.

    Args:
        data (pandas.DataFrame): Historical data containing columns like 'symbol', 'close', etc.
        short_window (int): The window size for the short-term moving average.
        long_window (int): The window size for the long-term moving average.

    Returns:
        dict: A dictionary where keys are trading symbols and values are generated buy/sell signals.
              Possible signal values are 'Buy', 'Sell', or 'No signal'.
    """
    signals = {}

    # Append rolling calculations to the original DataFrame
    data['short_ma'] = data.groupby('symbol')['close'].rolling(window=short_window).mean().droplevel(level=0)
    data['long_ma'] = data.groupby('symbol')['close'].rolling(window=long_window).mean().droplevel(level=0)

    # Generate initial buy/sell signals based on moving average crossovers
    data['signal'] = data.apply(
        lambda r: 'Buy' if r.short_ma > r.long_ma else ('Sell' if r.short_ma < r.long_ma else 'No signal'),
        axis='columns')

    # Identify crossover points
    data['signal_lag_1'] = data.groupby('symbol')['signal'].shift(1)
    data.loc[data['signal_lag_1'].isnull(), ['signal_lag_1']] = 'No signal'

    # Adjust signals for crossovers
    data['signal'] = data.apply(
        lambda r: 'Buy' if r.signal == 'Buy' and r.signal_lag_1 == 'Sell' else (
            'Sell' if r.signal == 'Sell' and r.signal_lag_1 == 'Buy' else 'No signal'),
        axis='columns')

    data = data.drop('signal_lag_1', axis=1)

    # Extract final signals for each symbol
    for i in data.groupby('symbol').signal.last().index:
        signals[i] = data.groupby('symbol').signal.last().loc[i]

    return signals
