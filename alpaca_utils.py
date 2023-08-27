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

    def get_historical_data(self, symbols, timeframe, start_date, end_date, chunk_size):
        """
            Retrieve historical data for a given symbol within a specified timeframe.

            This method retrieves historical data for the specified trading symbol over a given timeframe,
            using the provided chunk size to manage data retrieval in smaller segments.

            Args:
                symbols (str or list): The trading symbol(s) for which to retrieve historical data.
                              It can be a single symbol as a string or a list of symbols.
                timeframe (str): The desired timeframe for the historical data (e.g., '1D' for daily, '1H' for hourly).
                start_date (datetime.datetime): The start date of the historical data range.
                end_date (datetime.datetime): The end date of the historical data range.
                chunk_size (str): The size of data chunks to retrieve and process at a time (e.g., '250D').

            Returns:
                pandas.DataFrame: A DataFrame containing the retrieved historical data.
            """
        # Use Dask to parallelize and manage data retrieval in chunks
        df = dd.from_delayed([
            dask.delayed(self._get_historical_data_chunk)(symbols, timeframe, chunk_start, chunk_end)
            for chunk_start, chunk_end in self._generate_chunk_intervals(start_date, end_date, chunk_size)
        ])
        # Compute the Dask DataFrame to obtain the final result
        return df.compute()

    @staticmethod
    def _generate_chunk_intervals(start_date, end_date, chunk_size):
        """
        Generate intervals for data retrieval in chunks within a specified date range.

        This static method takes a start date, an end date, and a chunk size, and generates
        a list of intervals to retrieve data in smaller chunks within the specified date range.

        Args:
            start_date (datetime.datetime): The start date of the date range.
            end_date (datetime.datetime): The end date of the date range.
            chunk_size (str): The size of each chunk interval (e.g., '7D' for 7 days, '1M' for 1 month).

        Returns:
            list: A list of tuples representing intervals for data retrieval. Each tuple contains
                  a start and end date defining the range of data to be retrieved in a chunk.
        """
        # Generate date ranges using pandas
        ranges = pd.date_range(start=start_date, end=end_date, freq=chunk_size)

        # Append the end date to ensure coverage of the entire range
        ranges = ranges.append(pd.DatetimeIndex([end_date]))

        # Generate chunk intervals using the ranges
        chunk_intervals = [(rng, ranges[min(i + 1, len(ranges) - 1)]) for i, rng in enumerate(ranges)][:-1]

        return chunk_intervals

    # def get_historical_data(self, symbols, timeframe, start_date, end_date):
    def _get_historical_data_chunk(self, symbols, timeframe, start_date, end_date):
        """
            Retrieve historical data chunk for the specified symbols within a given timeframe.

            This method queries the API to retrieve historical data for the provided symbols within the specified
            timeframe, starting from the start date and ending on the end date.

            Args:
                symbols (str or list): The trading symbol(s) for which to retrieve historical data.
                                      It can be a single symbol as a string or a list of symbols.
                timeframe (str): The desired timeframe for the hist. data (e.g., 'Day' for daily, 'Hour' for hourly).
                start_date (datetime.datetime): The start date of the historical data range.
                end_date (datetime.datetime): The end date of the historical data range.

            Returns:
                pandas.DataFrame: A DataFrame containing the retrieved historical data.
            """
        # Define a mapping for timeframes to corresponding values
        switcher = {
            'Day': TimeFrame.Day,
            'Hour': TimeFrame.Hour,
            'Minute': TimeFrame.Minute,
            'Month': TimeFrame.Month,
            'Week': TimeFrame.Week
        }

        # Construct request parameters for fetching historical data
        request_params = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=switcher[timeframe],
            start=start_date,
            end=end_date
        )

        # Get historical data using the provided API client
        bars = self.api_stock_client.get_stock_bars(request_params)

        # Return the historical data as a DataFrame
        return bars.df

    def get_account(self):
        """
           Retrieve and display account information for trading activities.

           This method queries the trading API to retrieve account information, including
           trading status, available buying power, and any trading restrictions.

           Returns:
               Account: An object containing information about the trading account.
           """
        # Get account information using the provided trading API client
        account = self.api_trading_client.get_account()

        # Check if our account is restricted from trading
        if account.trading_blocked:
            print('Account is currently restricted from trading.')

        # Display available buying power (check how much money we can use to open new positions)
        print('${} is available as buying power.'.format(account.buying_power))

        return account

    def get_position(self, symbol):
        """
        Retrieve information about an open position for a specific symbol.

        This method queries the trading API to retrieve information about an open position
        associated with the specified trading symbol.

        Args:
            symbol (str): The trading symbol for which to retrieve the open position information.

        Returns:
            Position or None: An object containing information about the open position, or None if no position is found.
        """
        try:
            # Attempt to retrieve the open position using the provided trading API client
            position = self.api_trading_client.get_open_position(symbol)
            return position
        except Exception as e:
            # Print an error message if the method encounters an exception
            print(f"Method hasn't been completed successfully: {e}. It was called for position {symbol}.")

        return None

    def restore_buying_power(self):
        """
            Restore buying power by closing all positions and canceling open orders.

            This method uses the trading API to close all open positions and cancel any
            open orders, effectively releasing locked funds and restoring buying power.

            Note:
                This operation involves closing all positions and canceling orders, which
                may result in significant changes to your portfolio and trading strategy.

            Warning:
                Executing this method will result in trading actions. Use with caution.

            """
        # Close all positions and cancel open orders using the provided trading API client
        self.api_trading_client.close_all_positions(cancel_orders=True)

    def place_market_order(self, side, symbol, qty):
        """
        Place a market order for buying or selling a specified quantity of a symbol.

        This method submits a market order request to the trading API to buy or sell the specified
        quantity of the given trading symbol. The order is executed at the current market price.

        Args:
            side (str): The side of the order, either 'buy' or 'sell'.
            symbol (str): The trading symbol for which to place the market order.
            qty (int): The quantity of shares or contracts to buy or sell.

        Note:
            Market orders are executed at the best available market price and may result in immediate
            execution. The final executed price may vary from the initial market order price.

        Warning:
            Executing market orders can result in immediate trades at potentially unexpected prices.
            Use with caution, especially during volatile market conditions.

        """
        # Prepare market order data using the provided parameters
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            time_in_force=TimeInForce.DAY  # Option 'gtc' is possible as well
        )

        # Submit the market order using the provided trading API client
        self.api_trading_client.submit_order(
            order_data=market_order_data
        )

    def place_stop_loss_order(self, side, symbol, qty, stop_loss_price):
        """
        Place a stop-loss order for buying or selling a specified quantity of a symbol at a certain price.

        This method submits a stop-loss order request to the trading API. A stop-loss order is designed to
        trigger a market order when the specified stop price is reached, in order to limit potential losses.

        Args:
            side (str): The side of the order, either 'buy' or 'sell'.
            symbol (str): The trading symbol for which to place the stop-loss order.
            qty (int): The quantity of shares or contracts to buy or sell.
            stop_loss_price (float): The price at which the stop-loss order will be triggered.

        Note:
            Stop-loss orders are not guaranteed to execute at the exact specified price. They are designed
            to trigger a market order when the stop price is reached, and the executed price may vary.

        Warning:
            Stop-loss orders may not be executed at the expected price during fast-moving or volatile market conditions.
            Use with caution and consider using additional risk management strategies.

        """
        # Prepare stop order data using the provided parameters
        stop_order_data = StopOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            time_in_force=TimeInForce.DAY,  # Option 'gtc' is possible as well
            stop_price=stop_loss_price
        )

        # Submit the stop-loss order using the provided trading API client
        self.api_trading_client.submit_order(
            order_data=stop_order_data
        )
