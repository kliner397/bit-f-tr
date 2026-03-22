def validate_trade(levels):
    entry_mid = (levels["entry_low"] + levels["entry_high"]) / 2

    risk = abs(entry_mid - levels["sl"])
    reward = abs(levels["tp2"] - entry_mid)

    if risk == 0:
        return False

    rr = reward / risk

    return rr >= 1.5