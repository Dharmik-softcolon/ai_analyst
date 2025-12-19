from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TradeSignal:
    symbol: str
    signal: str                 # BUY / SELL / HOLD
    timeframe: str              # DAILY
    strategy: str               # SupplyDemand + RSI + Volume

    entry_price: float
    stop_loss: float
    target_price: float

    score: int                  # A+ score
    confidence: str             # LOW / MEDIUM / HIGH

    zone_type: str              # DEMAND / SUPPLY
    zone_low: float
    zone_high: float

    created_at: datetime
    expiry_days: int = 30       # Max holding (~6 weeks)

    comment: Optional[str] = None

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "signal": self.signal,
            "timeframe": self.timeframe,
            "strategy": self.strategy,
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "target_price": self.target_price,
            "score": self.score,
            "confidence": self.confidence,
            "zone": {
                "type": self.zone_type,
                "low": self.zone_low,
                "high": self.zone_high
            },
            "created_at": self.created_at,
            "expiry_days": self.expiry_days,
            "comment": self.comment
        }
