import ccxt
import pandas as pd

exchange = ccxt.binance({
    "options": {"defaultType": "future"}
})


def get_top_futures_pairs(limit=50):
    markets = exchange.load_markets()

    pairs = []

    for symbol, data in markets.items():
        if (
            data.get("quote") == "USDT"
            and data.get("active")
            and data.get("contract")  # только фьючерсы
        ):
            pairs.append(symbol)

    # убираем мусор
    blacklist = ["DENT", "FUN", "CVC", "COS", "MTL"]

    filtered = [
        s for s in pairs
        if not any(b in s for b in blacklist)
    ]

    return filtered[:limit]


def get_ohlcv(symbol, timeframe, limit=150):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["ts", "open", "high", "low", "close", "volume"])
        return df
    except Exception:
        return pd.DataFrame()