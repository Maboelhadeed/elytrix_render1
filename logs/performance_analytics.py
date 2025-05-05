class PerformanceAnalytics:
    def __init__(self, trades):
        self.trades = trades

    def summary(self):
        wins = [t for t in self.trades if t["profit"] > 0]
        losses = [t for t in self.trades if t["profit"] <= 0]
        total = sum(t["profit"] for t in self.trades)
        return {
            "total_trades": len(self.trades),
            "win_rate": len(wins) / len(self.trades) * 100 if self.trades else 0,
            "total_profit": total,
            "avg_win": sum(t["profit"] for t in wins)/len(wins) if wins else 0,
            "avg_loss": sum(t["profit"] for t in losses)/len(losses) if losses else 0
        }
