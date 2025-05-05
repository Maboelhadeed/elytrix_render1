# run_backtest.py
# Run backtesting using mock OHLCV data and selected strategy

import json
from core.backtester import Backtester
from strategies.trend_following import TrendFollowingStrategy
from strategies.breakout import BreakoutStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.meme_sniper import MemeSniperStrategy

# Load test config
with open("config/test_config.json", "r") as f:
    config = json.load(f)

strategy_map = {
    "trend_following": TrendFollowingStrategy,
    "breakout": BreakoutStrategy,
    "mean_reversion": MeanReversionStrategy,
    "meme_sniper": MemeSniperStrategy
}

strategy_name = config["strategy"]
strategy_class = strategy_map.get(strategy_name)

if not strategy_class:
    raise ValueError(f"Strategy '{strategy_name}' not recognized.")

# Use mock data for backtesting
data_file = "data/mock_ohlcv.csv"

# Run the backtest
backtester = Backtester(strategy_class, config, data_file)
results = backtester.run()

print("Backtest Summary:")
print(f"Starting Balance: ${results['starting_balance']}")
print(f"Ending Balance:   ${results['ending_balance']}")
print(f"Total Trades:     {results['total_trades']}")

for trade in results["trades"]:
    print(f"Trade: Entry ${trade['entry']} → Exit ${trade['exit']} = Profit ${trade['profit']}")
