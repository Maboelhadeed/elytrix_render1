from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import yfinance as yf
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live_price")
def get_live_price(
    symbol: str = Query(...),
    market: str = Query("stock"),
    range: str = Query("1d"),
    interval: str = Query("1m"),
):
    try:
        yf_symbol = symbol.upper()
        data = yf.Ticker(yf_symbol).history(period=range, interval=interval)

        if data.empty:
            return {"error": f"No data found for {yf_symbol}"}

        chart = []
        for timestamp, row in data.iterrows():
            chart.append({
                "timestamp": timestamp.isoformat(),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
            })

        return {
            "symbol": yf_symbol,
            "price": chart[-1]["close"],
            "chart": chart
        }

    except Exception as e:
        return {"error": str(e)}
