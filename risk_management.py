def calculate_max_position_size(account, risk_percentage):
    capital = float(account.equity)
    max_position_size = capital * risk_percentage
    return max_position_size
