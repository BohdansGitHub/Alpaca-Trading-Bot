from strategies import moving_average_crossover_strategy
from risk_management import calculate_max_position_size
from portfolio_optimization import calculate_optimal_weights
from alpaca_utils import AlpacaAPI
from aws_utils import S3FileManager
from datetime import datetime, timedelta
import pandas as pd
import time
import configparser


def main():
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Alpaca API credentials and other parameters
    alpaca_api_key_id = config['ALPACA']['API_KEY']
    alpaca_api_secret_key = config['ALPACA']['API_SECRET']

    # Define parameters
    historical_period = config.getint('MAIN', 'HISTORICAL_PERIOD')
    chunk_size = config['MAIN']['CHUNK_SIZE']
    end_date_offset = config.getint('MAIN', 'END_DATE_OFFSET')
    increase_allocation = config.getfloat('MAIN', 'INCREASE_ALLOCATION')
    decrease_allocation = config.getfloat('MAIN', 'DECREASE_ALLOCATION')
    symbols = config['MAIN']['SYMBOLS'].replace(" ", "").split(',')
    short_window = config.getint('STRATEGY', 'SHORT_WINDOW')
    long_window = config.getint('STRATEGY', 'LONG_WINDOW')
    risk_percentage = config.getfloat('RISK_MANAGEMENT', 'RISK_PERCENTAGE')
    risk_free_rate = config.getfloat('PORTFOLIO_OPTIMIZATION', 'RISK_FREE_RATE')
    aws_data_source = config.getboolean('AWS', 'AWS_DATA_SOURCE')
    aws_data_upload = config.getboolean('AWS', 'AWS_DATA_UPLOAD')
    bucket_name = config['AWS']['BUCKET_NAME']
    local_file = config['AWS']['LOCAL_FILE']
    aws_file = config['AWS']['AWS_FILE']

    # Initialize Alpaca API
    alpaca = AlpacaAPI(api_key=alpaca_api_key_id, api_secret=alpaca_api_secret_key)

    # Create an offset of n Business days
    offset = pd.tseries.offsets.BusinessDay(n=round(historical_period))

    # getting start_date and end_date by subtracting offset
    start_date = (datetime.utcnow() - offset).to_pydatetime()
    end_date = datetime.utcnow() - timedelta(minutes=end_date_offset)  # change to 0 to source most recent data

    # If using AWS as the data source, download the data from S3
    if aws_data_source:
        s3_manager = S3FileManager()
        s3_manager.download_file(bucket_name, local_file, aws_file)
        data = pd.read_csv(local_file)
    else:  # Otherwise, fetch data using Alpaca API
        data = alpaca.get_historical_data(symbols, 'Day', start_date, end_date, chunk_size)
        if aws_data_upload:  # Upload fetched data to AWS if configured
            data.to_csv(local_file)
            s3_manager = S3FileManager()
            s3_manager.upload_file(local_file, bucket_name, aws_file)

    # Execute moving average crossover strategy
    signals = moving_average_crossover_strategy(data, short_window, long_window)

    # Calculate optimal weights and position size
    optimal_weights = calculate_optimal_weights(data, risk_free_rate)

    # Combine strategies and adjust portfolio allocation
    allocation_weights = optimal_weights.copy()
    for symbol, signal in signals.items():
        if signal == 'Buy':
            allocation_weights[symbol] *= increase_allocation  # Increase allocation by n%
        elif signal == 'Sell':
            allocation_weights[symbol] *= decrease_allocation  # Decrease allocation by n%

    # Normalize allocation weights
    total_weight = sum(allocation_weights.values())
    for symbol in allocation_weights:
        allocation_weights[symbol] /= total_weight

    # Calculate available cash
    alpaca.restore_buying_power()
    account = alpaca.get_account()
    available_cash = float(account.buying_power)
    max_trade_amount = calculate_max_position_size(account, risk_percentage)

    # Calculate target dollar amounts to invest in each asset
    target_investments = {symbol: available_cash * allocation_weight for symbol, allocation_weight in
                          allocation_weights.items()}

    # Normalize target investments (total of absolute values of target investments <= available_cash)
    abs_total_investments = sum([abs(value) for value in target_investments.values()])
    for symbol in target_investments:
        target_investments[symbol] = min(max_trade_amount,
                                         target_investments[symbol] * (available_cash / abs_total_investments))

    # Place orders based on target_investments
    for symbol, target_amount in target_investments.items():
        current_price = data['close'][symbol].iloc[-1]
        shares_qty = int(target_amount / current_price)
        if shares_qty > 0:
            alpaca.place_market_order(side='buy', symbol=symbol, qty=shares_qty)

    print("Orders placed based on allocation weights and strategy signals. Time: ", datetime.utcnow().ctime())


if __name__ == "__main__":
    while True:
        main()
        # Wait for some time (e.g., 1 day) before checking again
        time.sleep(86400)
