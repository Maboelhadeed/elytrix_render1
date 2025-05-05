from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import requests
from datetime import datetime, timedelta

app = FastAPI()

# CORS for frontend access (like Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Alpaca API keys (replace with env vars in production)
ALPACA_API_KEY = "AKK343CVU61TVJJB6CBP"
ALPACA_SECRET_KEY = "JbuxU7Xb2I5doAd58oetqkJyVBxDu2BYa8bHkRKF"
HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
}
BASE_URL = "https://data.alpaca.markets/v2"

@app.get("/")
def home():
    return {"status": "Elytrix Chart Backend is running."}

@app.get("/market_data")
def get_market_data(
    symbol: str = Query(...),
    asset_type: str = Query("stock"),  # "stock" or "crypto"
    timeframe: str = Query("1Min"),    # "1Min", "5Min", "1Hour", etc.
    limit: int = Query(30)
):
    # Build request URL for Alpaca
    if asset_type == "crypto":
        url = f"{BASE_URL}/crypto/bars?symbols={symbol}&timeframe={timeframe}&limit={limit}"
    else:
        url = f"{BASE_URL}/stocks/{symbol}/bars?timeframe={timeframe}&limit={limit}"

    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        data = res.json()

        if asset_type == "crypto":
            bars = data.get("bars", {}).get(symbol.upper(), [])
        else:
            bars = data.get("bars", [])

        if not bars:
            return {"error": "No data found for symbol"}

        latest_price = bars[-1]["c"]
        chart_data = [{"timestamp": b["t"], "price": b["c"]} for b in bars]

        return {
            "symbol": symbol.upper(),
            "price": latest_price,
            "chart": chart_data
        }

    except Exception as e:
        return {"error": str(e)}
from fastapi import Request
from datetime import datetime
import httpx

# Your Alpaca credentials
ALPACA_API_KEY = "AKK343CVU61TVJJB6CBP"
ALPACA_SECRET_KEY = "JbuxU7Xb2I5doAd58oetqkJyVBxDu2BYa8bHkRKF"
ALPACA_DATA_URL = "https://data.alpaca.markets"

# CoinGecko base URL
COINGECKO_URL = "https://api.coingecko.com/api/v3"

@app.get("/live_price")
async def get_live_price(symbol: str, market: str = "stock"):
    try:
        if market.lower() == "stock":
            headers = {
                "APCA-API-KEY-ID": ALPACA_API_KEY,
                "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY,
            }
            async with httpx.AsyncClient() as client:
                url = f"{ALPACA_DATA_URL}/v2/stocks/{symbol}/bars?timeframe=1Min&limit=20"
                r = await client.get(url, headers=headers)
                bars = r.json().get("bars", [])
                chart = [{"timestamp": b["t"], "price": b["c"]} for b in bars]
                latest_price = chart[-1]["price"] if chart else None
                return {
                    "symbol": symbol.upper(),
                    "price": latest_price,
                    "chart": chart
                }

        elif market.lower() == "crypto":
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{COINGECKO_URL}/simple/price?ids={symbol.lower()}&vs_currencies=usd")
                price = r.json().get(symbol.lower(), {}).get("usd", None)

                chart_resp = await client.get(f"{COINGECKO_URL}/coins/{symbol.lower()}/market_chart?vs_currency=usd&days=1&interval=hourly")
                prices = chart_resp.json().get("prices", [])
                chart = [{"timestamp": datetime.utcfromtimestamp(p[0] / 1000).isoformat(), "price": round(p[1], 2)} for p in prices]

                return {
                    "symbol": symbol.upper(),
                    "price": price,
                    "chart": chart
                }

        else:
            return {"error": "Unsupported market type. Use 'stock' or 'crypto'."}

    except Exception as e:
        return {"error": str(e)}
