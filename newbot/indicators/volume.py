def average_volume(series, period=20):
    return series.rolling(period).mean()