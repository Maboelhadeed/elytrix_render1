# trend_following.py
# Sample trend-following strategy module

class TrendFollowingStrategy:
    def __init__(self, config):
        self.config = config
        self.prev_price = None

    def generate_signals(self, market_data):
        current_price = market_data["close"]
        signal = None

        if self.prev_price is not None:
            if current_price > self.prev_price:
                signal = {"action": "buy", "price": current_price}
            elif current_price < self.prev_price:
                signal = {"action": "sell", "price": current_price}

        self.prev_price = current_price
        return signal
