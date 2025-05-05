from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

# Allow all origins for now – you can restrict to Vercel domain later
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
def get_live_price(symbol: str = Query(...), market: str = Query("stock")):
    try:
        if market.lower() == "crypto":
            yf_symbol = symbol.upper() + "-USD"
        else:
            yf_symbol = symbol.upper()

        ticker = yf.Ticker(yf_symbol)

        hist = ticker.history(period="1d", interval="5m")
        if hist.empty:
            return {"error": f"No data found for {symbol} from Yahoo Finance."}

        current_price = round(hist["Close"].iloc[-1], 2)

        chart_data = [
            {
                "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "price": round(price, 2)
            }
            for dt, price in zip(hist.index, hist["Close"])
        ]

        return {
            "symbol": symbol.upper(),
            "price": current_price,
            "chart": chart_data
        }

    except Exception as e:
        return {"error": f"Failed to fetch data for {symbol}: {str(e)}"}
