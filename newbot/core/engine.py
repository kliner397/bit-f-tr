from core.data.market_data_builder import build_market_data
from core.execution.position_engine import get_position_plan


def run(symbol="BTC/USDT"):
    # === 1. MARKET DATA ===
    data = build_market_data(symbol)

    if data is None:
        return {
            "symbol": symbol,
            "decision": "NONE",
            "confidence": 0.0,
            "score": 0.0,
            "position": None
        }

    # === 2. SCORING ===
    score = 0

    # --- TREND 1H ---
    if data["price"] > data["ema_1h"]:
        score += 10
    else:
        score -= 10

    # --- TREND 4H ---
    if data["price"] > data["ema_4h"]:
        score += 15
    else:
        score -= 15

    # --- RSI ---
    rsi = data["rsi_15m"]
    if rsi < 30:
        score += 10
    elif rsi > 70:
        score -= 10

    # --- VOLUME ---
    if data["volume"] > data["avg_volume"]:
        score += 5

    # --- VOLATILITY ---
    if data["atr"] > data["price"] * 0.005:
        score += 5

    # === 3. DECISION ===
    abs_score = abs(score)

    if abs_score < 15:
        decision = "NONE"
        confidence = abs_score
    else:
        direction = "LONG" if score > 0 else "SHORT"

        if abs_score < 25:
            strength = "WEAK"
        elif abs_score < 35:
            strength = "MEDIUM"
        else:
            strength = "STRONG"

        decision = f"{direction}_{strength}"
        confidence = abs_score

    # === 4. POSITION ===
    position = None

    if decision != "NONE":
        try:
            position = get_position_plan(data, decision)
        except Exception as e:
            print(f"Position error for {symbol}: {e}")
            position = None

    # === 5. RESULT ===
    return {
        "symbol": symbol,
        "decision": decision,
        "confidence": round(confidence, 2),
        "score": round(score, 2),
        "position": position
    }
