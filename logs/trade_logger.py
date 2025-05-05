class TradeLogger:
    def __init__(self):
        self.trades = []

    def log_trade(self, trade):
        self.trades.append(trade)

    def export(self):
        return self.trades
