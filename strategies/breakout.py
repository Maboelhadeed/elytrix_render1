# breakout.py
# Simple breakout strategy that buys when price breaks above previous high

class BreakoutStrategy:
    def __init__(self, config):
        self.config = config
        self.recent_high = None
        self.recent_low = None
        self.lookback = config.get("lookback", 3)
        self.history = []

    def generate_signals(self, market_data):
        current_price = market_data["close"]
        self.history.append(current_price)

        if len(self.history) > self.lookback:
            self.history.pop(0)

        signal = None
        if len(self.history) == self.lookback:
            high = max(self.history)
            low = min(self.history)

            if current_price > high:
                signal = {"action": "buy", "price": current_price, "reason": "breakout_above"}
            elif current_price < low:
                signal = {"action": "sell", "price": current_price, "reason": "breakout_below"}

        return signal
