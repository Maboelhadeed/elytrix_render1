# strategy_manager.py
# Loads and manages strategies dynamically

class StrategyManager:
    def __init__(self, config):
        strategy_class = self._load_strategy_class(config['strategy'])
        self.strategy = strategy_class(config)

    def _load_strategy_class(self, strategy_name):
        # Placeholder for dynamic loading, can be replaced with importlib
        if strategy_name == "trend_following":
            from strategies.trend_following import TrendFollowingStrategy
            return TrendFollowingStrategy
        raise ValueError(f"Unknown strategy: {strategy_name}")

    def generate_signal(self, market_data):
        return self.strategy.generate_signals(market_data)
