def calculate_atr(df, period=14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    tr = high_low.combine(high_close, max).combine(low_close, max)

    atr = tr.rolling(period).mean()
    return atr