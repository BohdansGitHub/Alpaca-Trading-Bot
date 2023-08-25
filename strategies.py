def moving_average_crossover_strategy(data, short_window, long_window):
    signals = {}
    # Append the rolling calculations to the original DataFrame
    data['short_ma'] = data.groupby('symbol')['close'].rolling(window=short_window).mean().droplevel(level=0)
    data['long_ma'] = data.groupby('symbol')['close'].rolling(window=long_window).mean().droplevel(level=0)

    data['signal'] = data.apply(
        lambda r: 'Buy' if r.short_ma > r.long_ma else ('Sell' if r.short_ma < r.long_ma else 'No signal'),
        axis='columns')

    # Find cross points
    data['signal_lag_1'] = data.groupby('symbol')['signal'].shift(1)
    data.loc[data['signal_lag_1'].isnull(), ['signal_lag_1']] = 'No signal'

    data['signal'] = data.apply(
        lambda r: 'Buy' if r.signal == 'Buy' and r.signal_lag_1 == 'Sell' else (
            'Sell' if r.signal == 'Sell' and r.signal_lag_1 == 'Buy' else 'No signal'),
        axis='columns')

    data = data.drop('signal_lag_1', axis=1)

    for i in data.groupby('symbol').signal.last().index:
        signals[i] = data.groupby('symbol').signal.last().loc[i]

    return signals
