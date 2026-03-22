from analytics.levels import get_swing_levels
from analytics.liquidity import detect_liquidity_zones, find_nearest_liquidity


def get_position_plan(data, decision):
    """
    Формирует торговый план:
    - зона входа
    - SL
    - TP
    """

    price = data["price"]

    # === ПАРСИНГ РЕШЕНИЯ ===
    try:
        direction, strength = decision.split("_")
    except:
        return None

    # === ЛИКВИДНОСТЬ ===
    high_zones, low_zones = detect_liquidity_zones(data)
    nearest_above, nearest_below = find_nearest_liquidity(price, high_zones, low_zones)

    swing_high, swing_low = get_swing_levels(data)

    if swing_high is None or swing_low is None:
        return None

    # === ATR ===
    atr = data["atr"]

    # === ЛОГИКА ===

    if direction == "LONG":
        entry_low = price * 0.995
        entry_high = price * 1.005

        sl = swing_low - atr * 0.5

        tp1 = price + atr * 2
        tp2 = price + atr * 4
        tp3 = price + atr * 6

    elif direction == "SHORT":
        entry_low = price * 0.995
        entry_high = price * 1.005

        sl = swing_high + atr * 0.5

        tp1 = price - atr * 2
        tp2 = price - atr * 4
        tp3 = price - atr * 6

    else:
        return None

    # === ОКРУГЛЕНИЕ ===
    return {
        "entry_zone": (round(entry_low, 4), round(entry_high, 4)),
        "sl": round(sl, 4),
        "tp1": round(tp1, 4),
        "tp2": round(tp2, 4),
        "tp3": round(tp3, 4),
    }
