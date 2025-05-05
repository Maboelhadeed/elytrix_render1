# engine.py
# Main controller that ties all modules together

from core.strategy_manager import StrategyManager
from core.data_feed import MarketDataFeed
from core.execution_engine import ExecutionEngine
from core.logger import Logger

class ElytrixEngine:
    def __init__(self, config):
        self.config = config
        self.strategy_manager = StrategyManager(config)
        self.data_feed = MarketDataFeed(config)
        self.execution_engine = ExecutionEngine(config)
        self.logger = Logger()

    def run(self):
        self.logger.log("Elytrix Engine started.")
        while True:
            market_data = self.data_feed.get_latest_data()
            signal = self.strategy_manager.generate_signal(market_data)
            if signal:
                self.execution_engine.execute(signal)
