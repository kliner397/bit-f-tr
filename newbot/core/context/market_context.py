def get_market_context(features):
    trend = features.get("trend", 0)

    if trend >= 2:
        return "strong_trend"
    elif trend <= -2:
        return "strong_downtrend"
    else:
        return "range"