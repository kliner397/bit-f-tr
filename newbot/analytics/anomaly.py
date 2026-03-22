def detect_pump_dump(df):
    close = df["close"]

    change = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]

    pump = change > 0.03
    dump = change < -0.03

    return pump, dump
