# market_data_interface.py
# Unified interface for Elytrix to fetch either backtest data or live data

from core.live_data_feed import LiveDataFeed
from core.binance_data_feed import BinanceDataFeed
import csv

class MarketDataInterface:
    def __init__(self, config):
        self.mode = config.get("mode", "backtest")
        self.source = config.get("data_source", "csv")
        self.config = config
        self.pointer = 0
        self.history = []

        if self.mode == "backtest":
            file_path = config.get("csv_path", "data/mock_ohlcv.csv")
            with open(file_path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.history.append({
                        "timestamp": row["timestamp"],
                        "open": float(row["open"]),
                        "high": float(row["high"]),
                        "low": float(row["low"]),
                        "close": float(row["close"]),
                        "volume": float(row["volume"])
                    })
        elif self.mode == "live":
            if self.source == "binance":
                self.feed = BinanceDataFeed(symbol=config.get("symbol", "BTCUSDT"))
            else:
                self.feed = LiveDataFeed(
                    symbol=config.get("symbol", "AAPL"),
                    api_key=config.get("api_key"),
                    interval=config.get("interval", "1min")
                )

    def get_next(self):
        if self.mode == "backtest":
            if self.pointer < len(self.history):
                data = self.history[self.pointer]
                self.pointer += 1
                return data
            else:
                return None  # No more data
        elif self.mode == "live":
            return self.feed.get_latest_data()
