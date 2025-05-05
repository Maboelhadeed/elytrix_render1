class SLTPManager:
    def __init__(self, sl_pct=2.0, tp_pct=4.0):
        self.sl_pct = sl_pct
        self.tp_pct = tp_pct

    def get_sl_tp(self, entry_price):
        sl = entry_price * (1 - self.sl_pct / 100)
        tp = entry_price * (1 + self.tp_pct / 100)
        return sl, tp
