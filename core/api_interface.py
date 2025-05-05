from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

# CORS for frontend on Vercel or local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Elytrix backend is running."}

@app.get("/live_price")
def live_price(symbol: str = Query(...), market: str = Query("stock")):
    try:
        # Format symbol for Yahoo Finance
        if market.lower() == "crypto":
            full_symbol = f"{symbol.upper()}-USD"
        elif market.lower() == "forex":
            full_symbol = f"{symbol.upper()}=X"
        else:
            full_symbol = symbol.upper()

        ticker = yf.Ticker(full_symbol)
        hist = ticker.history(period="1d", interval="5m")

        if hist.empty:
            return {"error": f"No data found for {full_symbol}"}

        # Use last closing price
        latest = hist.iloc[-1]
        price = round(latest["Close"], 2)

        # Build OHLC chart data
        chart = [
            {
                "timestamp": ts.isoformat(),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
            }
            for ts, row in hist.iterrows()
        ]

        return {
            "symbol": symbol.upper(),
            "price": price,
            "chart": chart
        }

    except Exception as e:
        return {"error": str(e)}
