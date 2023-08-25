from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, StopOrderRequest
from alpaca.trading.enums import TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import dask.dataframe as dd
import dask
import pandas as pd


class AlpacaAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_trading_client = TradingClient(self.api_key, self.api_secret, paper=True)
        self.api_stock_client = StockHistoricalDataClient(self.api_key, self.api_secret)

    def get_historical_data(self, symbol, timeframe, start_date, end_date):
        df = dd.from_delayed([
            dask.delayed(self._get_historical_data_chunk)(symbol, timeframe, chunk_start, chunk_end)
            for chunk_start, chunk_end in self._generate_chunk_intervals(start_date, end_date)
        ])
        return df.compute()

    @staticmethod
    def _generate_chunk_intervals(start_date, end_date, chunk_size='250D'):
        ranges = pd.date_range(start=start_date, end=end_date, freq=chunk_size)
        ranges = ranges.append(pd.DatetimeIndex([end_date]))
        chunk_intervals = [(rng, ranges[min(i + 1, len(ranges) - 1)]) for i, rng in enumerate(ranges)][:-1]
        return chunk_intervals

    # def get_historical_data(self, symbols, timeframe, start_date, end_date):
    def _get_historical_data_chunk(self, symbols, timeframe, start_date, end_date):
        # Define time frame in requested format
        switcher = {
            'Day': TimeFrame.Day,
            'Hour': TimeFrame.Hour,
            'Minute': TimeFrame.Minute,
            'Month': TimeFrame.Month,
            'Week': TimeFrame.Week
        }
        # Get historical data
        request_params = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=switcher[timeframe],
            start=start_date,
            end=end_date
        )
        bars = self.api_stock_client.get_stock_bars(request_params)
        return bars.df

    def get_account(self):
        # Get our account information.
        account = self.api_trading_client.get_account()

        # Check if our account is restricted from trading.
        if account.trading_blocked:
            print('Account is currently restricted from trading.')

        # Check how much money we can use to open new positions.
        print('${} is available as buying power.'.format(account.buying_power))

        return account

    def get_position(self, symbol):
        try:
            position = self.api_trading_client.get_open_position(symbol)
            return position
        except Exception as e:
            print(f"Method hasn't been completed successfully: {e}. It was called for position {symbol}.")

        return None

    def restore_buying_power(self):
        # closes all position AND also cancels all open orders
        self.api_trading_client.close_all_positions(cancel_orders=True)

    def place_market_order(self, side, symbol, qty):
        # preparing orders
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            time_in_force=TimeInForce.DAY  # Option 'gtc' is possible as well
        )
        # Market order
        self.api_trading_client.submit_order(
            order_data=market_order_data
        )

    def place_stop_loss_order(self, side, symbol, qty, stop_loss_price):
        # preparing orders
        stop_order_data = StopOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            time_in_force=TimeInForce.DAY,  # Option 'gtc' is possible as well
            stop_price=stop_loss_price
        )
        # Stop order
        self.api_trading_client.submit_order(
            order_data=stop_order_data
        )
