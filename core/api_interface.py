from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import yfinance as yf
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace with your Vercel domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live_price")
def get_price(
    symbol: str = Query(...),
    market: str = Query("stock"),
    range: str = Query("1d"),
    interval: str = Query("1m")
):
    yf_symbol = symbol.upper()
    if market == "crypto":
        yf_symbol = f"{yf_symbol}-USD"

    try:
        ticker = yf.Ticker(yf_symbol)
        hist = ticker.history(period=range, interval=interval)

        if hist.empty:
            return {"error": "No data available for this symbol."}

        last_price = hist["Close"].iloc[-1]
        chart = [
            {
                "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
            }
            for timestamp, row in hist.iterrows()
        ]

        return {
            "symbol": symbol.upper(),
            "price": float(last_price),
            "chart": chart,
        }

    except Exception as e:
        return {"error": str(e)}
