# run_simulation.py
# Runs the Elytrix engine with test config

import json
from core.engine import ElytrixEngine

# Load config
with open("config/test_config.json", "r") as f:
    config = json.load(f)

# Start engine
engine = ElytrixEngine(config)
engine.run()
