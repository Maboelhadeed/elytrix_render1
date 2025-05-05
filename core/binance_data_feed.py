# binance_data_feed.py
# Fetches live crypto data from Binance public API

import requests

class BinanceDataFeed:
    def __init__(self, symbol="BTCUSDT", interval="1m"):
        self.symbol = symbol
        self.interval = interval

    def get_latest_data(self):
        url = f"https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval={self.interval}&limit=1"
        response = requests.get(url)
        if response.status_code == 200:
            kline = response.json()[0]
            return {
                "timestamp": kline[0],
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5])
            }
        else:
            return {"error": "Failed to fetch data from Binance."}
