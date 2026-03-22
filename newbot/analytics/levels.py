def get_swing_levels(data, lookback=20):
    """
    Находит зоны ликвидности (локальные максимумы и минимумы)
    """

    highs = data.get("recent_highs", [])
    lows = data.get("recent_lows", [])

    if not highs or not lows:
        return None, None

    # Берем последние значения
    swing_high = max(highs[-lookback:])
    swing_low = min(lows[-lookback:])

    return swing_high, swing_low
