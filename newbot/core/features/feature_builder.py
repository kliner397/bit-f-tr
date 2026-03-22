from analytics.levels import get_levels
from analytics.liquidity import get_liquidity_zones
def build_features(market_data):
    features = {}

    price = market_data["price"]

    # === TREND (1h + 4h) ===
    trend_score = 0

    trend_score += 2 if price > market_data["ema_4h"] else -2
    trend_score += 1 if price > market_data["ema_1h"] else -1

    features["trend"] = trend_score

    # === ENTRY (15m RSI) ===
    rsi_15m = market_data["rsi_15m"]

    if rsi_15m < 30:
        features["entry_rsi"] = 2
    elif rsi_15m > 70:
        features["entry_rsi"] = -2
    else:
        features["entry_rsi"] = 0

    # === VOLUME ===
    volume = market_data["volume"]
    avg_volume = market_data["avg_volume"]

    spike = volume / avg_volume if avg_volume > 0 else 1

    features["volume_spike"] = spike

    # === LEVELS ===
    levels = get_levels(df_1h)
    f["support"] = levels["support"]
    f["resistance"] = levels["resistance"]

    # === LIQUIDITY ===
    liquidity = get_liquidity_zones(df_5m)
    f["liquidation_zone_above"] = liquidity["above"]
    f["liquidation_zone_below"] = liquidity["below"]


    return features