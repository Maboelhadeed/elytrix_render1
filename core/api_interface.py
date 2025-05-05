from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import httpx
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Your Alpaca keys (inserted back as provided)
ALPACA_API_KEY = "AKK343CVU61TVJJB6CBP"
ALPACA_SECRET_KEY = "JbuxU7Xb2I5doAd58oetqkJyVBxDu2BYa8bHkRKF"

@app.get("/live_price")
async def get_live_price(symbol: str, market: str = "stock"):
    end = datetime.utcnow()
    start = end - timedelta(days=2)

    if market == "crypto":
        data = yf.download(f"{symbol}-USD", start=start, end=end, interval="1h")
        if data.empty:
            return {"error": "Crypto data not found."}
        chart = [
            {
                "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
            }
            for ts, row in data.iterrows()
        ]
        return {"symbol": symbol, "price": float(data['Close'][-1]), "chart": chart}

    else:
        headers = {
            "APCA-API-KEY-ID": AKK343CVU61TVJJB6CBP,
            "APCA-API-SECRET-KEY": JbuxU7Xb2I5doAd58oetqkJyVBxDu2BYa8bHkRKF,
        }
        async with httpx.AsyncClient() as client:
            url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars"
            params = {
                "timeframe": "1Hour",
                "start": start.isoformat() + "Z",
                "end": end.isoformat() + "Z",
                "limit": 100
            }
            response = await client.get(url, headers=headers, params=params)
            if response.status_code != 200:
                return {"error": "Stock data not found from Alpaca."}
            data = response.json()
            bars = data.get("bars", [])
            if not bars:
                return {"error": "No bars returned."}

            chart = [
                {
                    "timestamp": bar["t"],
                    "open": bar["o"],
                    "high": bar["h"],
                    "low": bar["l"],
                    "close": bar["c"],
                }
                for bar in bars
            ]
            return {"symbol": symbol, "price": bars[-1]["c"], "chart": chart}
