import pandas as pd
import numpy as np


def calculate_atr(df, period=14):
    high = df["high"]
    low = df["low"]
    close = df["close"]

    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean()

    return atr


def get_volatility_score(df):
    atr = calculate_atr(df)

    current_atr = atr.iloc[-1]
    price = df["close"].iloc[-1]

    atr_percent = (current_atr / price) * 100

    return {
        "atr": float(current_atr),
        "atr_percent": float(atr_percent)
    }


def is_market_active(df, min_atr_percent=0.05):
    """
    СНИЖЕННЫЙ ПОРОГ!
    Было 0.3 → стало 0.05
    """
    data = get_volatility_score(df)

    return data["atr_percent"] >= min_atr_percent
