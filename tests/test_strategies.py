import unittest
import pandas as pd
from strategies import moving_average_crossover_strategy


class TestMovingAverageCrossoverStrategy(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        data = pd.DataFrame({
            'symbol': ['AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL',
                       'GOOG', 'GOOG', 'GOOG', 'GOOG', 'GOOG', 'GOOG', 'GOOG', 'GOOG', 'GOOG', 'GOOG',
                       'MSFT', 'MSFT', 'MSFT', 'MSFT', 'MSFT', 'MSFT', 'MSFT', 'MSFT', 'MSFT', 'MSFT'],
            'timestamp': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
                          '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10',
                          '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
                          '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10',
                          '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
                          '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10'],
            'close': [150.0, 155.0, 160.0, 157.0, 159.0, 161.0, 162.0, 158.0, 155.0, 152.0,
                      2500.0, 2520.0, 2550.0, 2570.0, 2560.0, 2575.0, 2580.0, 2590.0, 2560.0, 2530.0,
                      300.0, 305.0, 310.0, 308.0, 307.0, 309.0, 308.0, 306.0, 312.0, 308.0]
        })

        # Set multi-index with names=['symbol', 'timestamp']
        data.set_index(['symbol', 'timestamp'], inplace=True)

        self.data = data
        self.short_window = 3
        self.long_window = 5

    def test_moving_average_crossover_strategy(self):
        # Test the moving_average_crossover_strategy function
        signals = moving_average_crossover_strategy(self.data, self.short_window, self.long_window)

        # Assert that the result is a dictionary
        self.assertIsInstance(signals, dict)

        # Assert that the dictionary has the expected symbols as keys
        expected_symbols = ['AAPL', 'GOOG', 'MSFT']
        self.assertCountEqual(list(signals.keys()), expected_symbols)

        # Assert that each value in the dictionary is one of the expected signal values
        expected_signal_values = ['Buy', 'Sell', 'No signal']
        for signal_value in signals.values():
            self.assertIn(signal_value, expected_signal_values)


if __name__ == '__main__':
    unittest.main()
