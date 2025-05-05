# backtester.py
# Runs historical data through a selected strategy and tracks performance

import csv

class Backtester:
    def __init__(self, strategy_class, strategy_config, data_file):
        self.strategy = strategy_class(strategy_config)
        self.data_file = data_file
        self.trades = []
        self.initial_balance = 1000
        self.balance = self.initial_balance
        self.position = None

    def run(self):
        with open(self.data_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                market_data = {
                    "timestamp": row["timestamp"],
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row["volume"])
                }

                signal = self.strategy.generate_signals(market_data)
                if signal:
                    self._process_signal(signal, market_data["close"], market_data["timestamp"])

        return {
            "starting_balance": self.initial_balance,
            "ending_balance": self.balance,
            "trades": self.trades,
            "total_trades": len(self.trades)
        }

    def _process_signal(self, signal, price, timestamp):
        if signal["action"] == "buy" and self.position is None:
            self.position = {"entry": price, "timestamp": timestamp}
        elif signal["action"] == "sell" and self.position:
            profit = price - self.position["entry"]
            self.balance += profit
            self.trades.append({
                "entry": self.position["entry"],
                "exit": price,
                "profit": profit,
                "entry_time": self.position["timestamp"],
                "exit_time": timestamp
            })
            self.position = None
