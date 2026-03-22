from core.config import LONG_THRESHOLD, SHORT_THRESHOLD, MAX_SCORE
from core.models.signal import Signal

def make_decision(symbol, score, context):
    side = "NONE"

    if score >= LONG_THRESHOLD:
        side = "LONG"
    elif score <= SHORT_THRESHOLD:
        side = "SHORT"

    confidence = min(abs(score) / MAX_SCORE * 100, 100)

    return Signal(
        symbol=symbol,
        side=side,
        score=score,
        confidence=confidence
    )