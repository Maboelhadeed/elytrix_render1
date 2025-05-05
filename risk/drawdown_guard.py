class DrawdownGuard:
    def __init__(self, max_drawdown=20.0):
        self.max_drawdown = max_drawdown
        self.high_watermark = None

    def check(self, balance):
        if self.high_watermark is None:
            self.high_watermark = balance
        drawdown = 100 * (self.high_watermark - balance) / self.high_watermark
        return drawdown < self.max_drawdown
