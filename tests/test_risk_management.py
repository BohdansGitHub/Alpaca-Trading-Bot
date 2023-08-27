import unittest
from risk_management import calculate_max_position_size


# Define MockAccount outside of the TestRiskManagement class
class MockAccount:
    def __init__(self, equity):
        self.equity = equity


class TestRiskManagement(unittest.TestCase):

    def test_calculate_max_position_size(self):
        # Test with a risk percentage of 0.02 (2%)
        account = MockAccount(equity=10000)
        risk_percentage = 0.02
        expected_max_position_size = 10000 * 0.02

        # Calculate the max position size using the function
        calculated_max_position_size = calculate_max_position_size(account, risk_percentage)

        # Assert that the calculated max position size matches the expected value
        self.assertEqual(calculated_max_position_size, expected_max_position_size)

    def test_calculate_max_position_size_zero_risk(self):
        # Test with a risk percentage of 0 (no risk)
        account = MockAccount(equity=5000)
        risk_percentage = 0.0
        expected_max_position_size = 0.0

        # Calculate the max position size using the function
        calculated_max_position_size = calculate_max_position_size(account, risk_percentage)

        # Assert that the calculated max position size is 0
        self.assertEqual(calculated_max_position_size, expected_max_position_size)


if __name__ == '__main__':
    unittest.main()
