class PositionSizer:
    def __init__(self, capital, risk_percent=1.0):
        self.capital = capital
        self.risk_percent = risk_percent

    def calculate_position_size(self, stop_loss_distance):
        risk_amount = (self.risk_percent / 100) * self.capital
        if stop_loss_distance > 0:
            return risk_amount / stop_loss_distance
        return 0
