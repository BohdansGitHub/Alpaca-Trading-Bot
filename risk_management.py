def calculate_max_position_size(account, risk_percentage):
    """
    Calculate the maximum position size based on available capital and risk percentage.

    This function takes an account object and a risk percentage as inputs and calculates
    the maximum position size that can be taken to adhere to the specified risk limit.

    Args:
        account (Account): An account object containing information about available capital.
        risk_percentage (float): The maximum percentage of capital to risk on a single position.

    Returns:
        float: The maximum position size that can be taken while adhering to the risk limit.
    """
    # Extract available equity from the account object
    capital = float(account.equity)

    # Calculate the maximum position size based on the capital and risk percentage
    max_position_size = capital * risk_percentage

    return max_position_size
