def calculate_ema(df, period=50):
    """
    Возвращает EMA (Series, не DataFrame!)
    """
    return df["close"].ewm(span=period, adjust=False).mean()
