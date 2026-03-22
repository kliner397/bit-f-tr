from dataclasses import dataclass

@dataclass
class Signal:
    symbol: str
    side: str
    score: float
    confidence: float
    levels: dict | None = None