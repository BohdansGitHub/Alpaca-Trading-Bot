import unittest
import pandas as pd
from portfolio_optimization import calculate_optimal_weights


class TestPortfolioOptimization(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        data = pd.DataFrame({
            'symbol': ['AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL',
                       'GOOG', 'GOOG', 'GOOG', 'GOOG', 'GOOG',
                       'MSFT', 'MSFT', 'MSFT', 'MSFT', 'MSFT'],
            'timestamp': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
                          '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
                          '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
            'open': [150.0, 155.0, 160.0, 157.0, 159.0,
                     2500.0, 2520.0, 2550.0, 2570.0, 2560.0,
                     300.0, 305.0, 310.0, 308.0, 307.0],
            'high': [155.0, 160.0, 165.0, 160.0, 162.0,
                     2550.0, 2570.0, 2600.0, 2580.0, 2580.0,
                     305.0, 310.0, 315.0, 312.0, 310.0],
            'low': [148.0, 153.0, 158.0, 153.0, 157.0,
                    2480.0, 2500.0, 2530.0, 2550.0, 2540.0,
                    295.0, 300.0, 305.0, 300.0, 302.0],
            'close': [152.0, 158.0, 162.0, 159.0, 161.0,
                      2520.0, 2550.0, 2580.0, 2560.0, 2570.0,
                      302.0, 308.0, 312.0, 306.0, 308.0],
            'volume': [1000000, 1200000, 900000, 1100000, 800000,
                       500000, 550000, 600000, 650000, 700000,
                       800000, 850000, 900000, 950000, 1000000],
            'trade_count': [100, 110, 95, 105, 90,
                            90, 95, 100, 105, 110,
                            70, 75, 80, 85, 90],
            'vwap': [153.0, 157.0, 161.0, 156.0, 159.0,
                     2535.0, 2560.0, 2590.0, 2575.0, 2585.0,
                     303.0, 306.0, 309.0, 303.5, 306.0]
        })

        # Set multi-index with names=['symbol', 'timestamp']
        data.set_index(['symbol', 'timestamp'], inplace=True)

        self.data = data
        self.risk_free_rate = 0.02  # Example risk-free rate

    def test_calculate_optimal_weights(self):
        # Test the calculate_optimal_weights function
        optimal_weights = calculate_optimal_weights(self.data, self.risk_free_rate)

        # Assert that the result is a dictionary
        self.assertIsInstance(optimal_weights, dict)

        # Assert that the dictionary has the expected symbols as keys
        expected_symbols = ['AAPL', 'GOOG', 'MSFT']
        self.assertCountEqual(list(optimal_weights.keys()), expected_symbols)

        # Assert that the weights are within valid bounds (between 0 and 1)
        for weight in optimal_weights.values():
            self.assertGreaterEqual(weight, 0)
            self.assertLessEqual(weight, 1)


if __name__ == '__main__':
    unittest.main()
