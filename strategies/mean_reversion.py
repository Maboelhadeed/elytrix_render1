# mean_reversion.py
# Strategy that buys when price is below average and sells when above

class MeanReversionStrategy:
    def __init__(self, config):
        self.config = config
        self.window = config.get("window", 5)
        self.prices = []

    def generate_signals(self, market_data):
        current_price = market_data["close"]
        self.prices.append(current_price)

        if len(self.prices) > self.window:
            self.prices.pop(0)

        signal = None
        if len(self.prices) == self.window:
            avg_price = sum(self.prices) / self.window
            if current_price < avg_price * 0.98:
                signal = {"action": "buy", "price": current_price, "reason": "below_mean"}
            elif current_price > avg_price * 1.02:
                signal = {"action": "sell", "price": current_price, "reason": "above_mean"}

        return signal
