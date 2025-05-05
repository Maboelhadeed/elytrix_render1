from fastapi import FastAPI, Query
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or replace "*" with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or replace "*" with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Available strategy names (expand this list as you implement them)
STRATEGIES = [
    "trend_following",
    "mean_reversion",
    "scalping",
    "rsi_divergence",
    "vwap",
    "volume_spike",
    "heikin_ashi",
    "meme_sniper"
]

@app.get("/")
def home():
    return {"status": "Elytrix API running."}

@app.get("/strategies")
def get_strategies():
    return {"available_strategies": STRATEGIES}

@app.get("/run")
def run_strategy(strategy: str = Query(...), mode: str = Query("backtest")):
    if strategy not in STRATEGIES:
        return {"error": f"Strategy '{strategy}' not found. Use /strategies to list available options."}
    
    # Simulated response (you will later connect real strategy logic here)
    return {
        "status": "running",
        "strategy": strategy,
        "mode": mode,
        "result": f"Simulated execution of {strategy} in {mode} mode"
    }
import requests
from fastapi import FastAPI, Query

ALPACA_API_KEY = "AKK343CVU61TVJJB6CBP"
ALPACA_SECRET_KEY = "JbuxU7Xb2I5doAd58oetqkJyVBxDu2BYa8bHkRKF"

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
}

@app.get("/live_price")
def get_live_price(symbol: str = Query(..., description="e.g. AAPL or EURUSD")):
    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return {"error": f"Failed to fetch price for {symbol}", "details": response.json()}

    data = response.json()
    quote = data.get("quote", {})
    return {
        "symbol": symbol.upper(),
        "price": quote.get("ap", "N/A"),
        "timestamp": quote.get("t", "N/A")
    }
