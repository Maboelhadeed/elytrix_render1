from fastapi import FastAPI, Query
from typing import List, Optional

app = FastAPI()

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
