def detect_liquidity_zones(data):
    """
    Определяем зоны ликвидности (скопления хай/лоу)
    """

    highs = data.get("recent_highs", [])
    lows = data.get("recent_lows", [])

    if not highs or not lows:
        return [], []

    # Берем уникальные уровни
    high_zones = list(set(highs))
    low_zones = list(set(lows))

    # Сортировка
    high_zones.sort(reverse=True)
    low_zones.sort()

    return high_zones, low_zones


def find_nearest_liquidity(price, high_zones, low_zones):
    """
    Находит ближайшие уровни ликвидности
    """

    nearest_above = None
    nearest_below = None

    # выше цены
    for level in high_zones:
        if level > price:
            nearest_above = level
            break

    # ниже цены
    for level in reversed(low_zones):
        if level < price:
            nearest_below = level
            break

    return nearest_above, nearest_below
