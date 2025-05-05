from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Elytrix backend running"}

@app.get("/live_price")
def live_price(
    symbol: str = Query(...),
    market: str = Query("stock"),
    interval: str = Query("5m"),
    range: str = Query("1d")
):
    try:
        # Format symbol for Yahoo Finance
        if market == "crypto":
            yf_symbol = f"{symbol.upper()}-USD"
        elif market == "forex":
            yf_symbol = f"{symbol.upper()}=X"
        else:
            yf_symbol = symbol.upper()

        # Fetch historical data
        ticker = yf.Ticker(yf_symbol)
        hist = ticker.history(interval=interval, period=range)

        if hist.empty:
            return {"error": f"No data found for {symbol} ({yf_symbol})"}

        last_price = round(hist["Close"].iloc[-1], 2)

        # Prepare chart data
        chart_data = [
            {
                "timestamp": i.isoformat(),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
            }
            for i, row in hist.iterrows()
        ]

        return {
            "symbol": symbol.upper(),
            "price": last_price,
            "chart": chart_data
        }

    except Exception as e:
        return {"error": str(e)}
