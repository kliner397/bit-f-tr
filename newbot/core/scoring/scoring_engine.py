from core.scoring.weights import WEIGHTS

def calculate_score(features):
    score = 0

    # === TREND ===
    trend_score = (
        features["htf_trend"] +
        features["mtf_trend"] +
        features["ltf_signal"]
    ) / 3
    score += trend_score * WEIGHTS["trend"]

    # === MOMENTUM (RSI) ===
    rsi = features["rsi"]
    if rsi < 30:
        momentum_score = 1
    elif rsi > 70:
        momentum_score = -1
    else:
        momentum_score = 0
    score += momentum_score * WEIGHTS["momentum"]

    # === VOLUME ===
    volume_score = 1 if features["volume_spike"] else 0
    score += volume_score * WEIGHTS["volume"]

    # === VOLATILITY ===
    volatility_score = features["atr_percent"]
    score += volatility_score * WEIGHTS["volatility"]

    # === LEVEL REACTION (НОВОЕ) ===
    price_position = 0

    if features["rsi"] < 35 and features["support"] > 0:
        price_position += 1

    if features["rsi"] > 65 and features["resistance"] > 0:
        price_position -= 1

    score += price_position * 10

    # === LIQUIDITY (НОВОЕ) ===
    if features["liquidation_zone_below"]:
        score += 8

    if features["liquidation_zone_above"]:
        score -= 8

    return round(score, 2)
