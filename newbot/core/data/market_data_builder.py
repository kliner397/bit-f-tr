from data.market_provider import get_ohlcv

from indicators.rsi import calculate_rsi
from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.volume import average_volume


def build_market_data(symbol):
    try:
        # === ЗАГРУЗКА ДАННЫХ ===
        df_15m = get_ohlcv(symbol, "15m")
        df_1h = get_ohlcv(symbol, "1h")
        df_4h = get_ohlcv(symbol, "4h")

        # Проверка
        if df_15m is None or df_1h is None or df_4h is None:
            return None

        if df_15m.empty or df_1h.empty or df_4h.empty:
            return None

        # === ИНДИКАТОРЫ ===

        # RSI
        df_15m["rsi"] = calculate_rsi(df_15m)
        float(df_15m["rsi"].iloc[-1])


        # ATR (волатильность)
        df_15m["atr"] = calculate_atr(df_15m)

        # EMA тренды
        df_1h["ema"] = calculate_ema(df_1h, 50)
        df_4h["ema"] = calculate_ema(df_4h, 100)

        # Объем
        df_15m["avg_volume"] = average_volume(df_15m["volume"])

        # === ЛИКВИДНОСТЬ ===
        recent_highs = df_15m["high"].tail(20).tolist()
        recent_lows = df_15m["low"].tail(20).tolist()

        # === ФОРМИРУЕМ DATA ===
        data = {
            "symbol": symbol,

            "price": float(df_15m["close"].iloc[-1]),

            "rsi_15m": float(df_15m["rsi"].iloc[-1]),

            "ema_1h": float(df_1h["ema"].iloc[-1]),
            "ema_4h": float(df_4h["ema"].iloc[-1]),

            "volume": float(df_15m["volume"].iloc[-1]),
            "avg_volume": float(df_15m["avg_volume"].iloc[-1]),

            "atr": float(df_15m["atr"].iloc[-1]),

            # ликвидность
            "recent_highs": recent_highs,
            "recent_lows": recent_lows,
        }

        return data

    except Exception as e:
        print(f"Error in build_market_data for {symbol}: {e}")
        return None
