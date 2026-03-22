def build_trade_levels(signal, market_data):
    price = market_data["price"]
    atr = market_data["atr"]

    highs = market_data["recent_highs"]
    lows = market_data["recent_lows"]

    if not highs or not lows:
        return None

    # берём последние уровни ликвидности
    last_high = max(highs[-5:])
    last_low = min(lows[-5:])

    if signal.side == "LONG":
        # === ENTRY ZONE ===
        entry_low = price - atr * 1.2
        entry_high = price

        # === SL за ликвидностью ===
        sl = last_low - atr * 0.5

        # === TP к ликвидности ===
        tp1 = last_high
        tp2 = last_high + atr
        tp3 = last_high + atr * 2

    elif signal.side == "SHORT":
        entry_high = price + atr * 1.2
        entry_low = price

        sl = last_high + atr * 0.5

        tp1 = last_low
        tp2 = last_low - atr
        tp3 = last_low - atr * 2

    else:
        return None

    return {
        "entry_low": entry_low,
        "entry_high": entry_high,
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
    }