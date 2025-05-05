from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Elytrix Market API running"}

@app.get("/live_price")
def live_price(symbol: str = Query(...), market: str = Query("stock")):
    try:
        data = yf.Ticker(symbol)
        hist = data.history(period="1d", interval="5m")
        if hist.empty:
            return {"error": f"No price data for {symbol}"}

        latest = hist.iloc[-1]
        price = round(latest["Close"], 2)
        chart = [
            {
                "timestamp": i.strftime("%Y-%m-%dT%H:%M:%S"),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
            }
            for i, row in hist.iterrows()
        ]

        return {"symbol": symbol.upper(), "price": price, "chart": chart}
    except Exception as e:
        return {"error": str(e)}
