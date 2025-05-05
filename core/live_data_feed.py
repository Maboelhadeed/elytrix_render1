# live_data_feed.py
# Module to fetch live market data from Alpha Vantage or Binance

import requests
import time

class LiveDataFeed:
    def __init__(self, source="alpha_vantage", api_key=None, symbol="AAPL", interval="1min"):
        self.source = source
        self.api_key = api_key
        self.symbol = symbol
        self.interval = interval

    def get_latest_data(self):
        if self.source == "alpha_vantage":
            url = (
                f"https://www.alphavantage.co/query?"
                f"function=TIME_SERIES_INTRADAY&symbol={self.symbol}&interval={self.interval}&apikey={self.api_key}&outputsize=compact"
            )
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                time_series = data.get(f"Time Series ({self.interval})", {})
                if time_series:
                    latest_time = sorted(time_series.keys())[-1]
                    entry = time_series[latest_time]
                    return {
                        "timestamp": latest_time,
                        "open": float(entry["1. open"]),
                        "high": float(entry["2. high"]),
                        "low": float(entry["3. low"]),
                        "close": float(entry["4. close"]),
                        "volume": float(entry["5. volume"]),
                    }
            return {"error": "Failed to fetch or parse Alpha Vantage data."}
        else:
            return {"error": "Unsupported data source."}
