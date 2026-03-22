def empty_features():
    return {
        "htf_trend": 0,
        "mtf_trend": 0,
        "ltf_signal": 0,

        "rsi": 50,
        "volume_spike": False,

        "volatility_level": 0.0,
        "volatility_spike": False,

        "pump_detected": False,
        "dump_detected": False,

        "funding_bias": 0.0,
        "oi_change": 0.0,

        "liquidation_zone_above": False,
        "liquidation_zone_below": False,
    }
