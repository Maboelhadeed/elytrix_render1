from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Elytrix API running."}

@app.get("/live_price")
def get_price(symbol: str = Query(...), market: str = Query("stock")):
    try:
        if market == "crypto":
            full_symbol = f"{symbol.upper()}-USD"
        elif market == "forex":
            full_symbol = f"{symbol.upper()}=X"
        else:
            full_symbol = symbol.upper()

        ticker = yf.Ticker(full_symbol)
        hist = ticker.history(period="1d", interval="5m")

        if hist.empty:
            return {"error": f"No price data found for {symbol} ({full_symbol})"}

        current_price = hist["Close"].iloc[-1]
        chart_data = [
            {
                "timestamp": ts.isoformat(),
                "price": float(price)
            }
            for ts, price in zip(hist.index, hist["Close"])
        ]

        return {
            "symbol": symbol.upper(),
            "price": round(float(current_price), 2),
            "chart": chart_data
        }

    except Exception as e:
        return {"error": str(e)}
