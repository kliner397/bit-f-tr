import pandas as pd

class CorrelationGuard:
    def __init__(self, btc_symbol="BTC/USDT:USDT"):
        self.btc_symbol = btc_symbol

    def analyze_market_health(self, exchange, provider):
        """Анализ состояния Биткоина (Предохранитель)"""
        try:
            # Грузим 20 свечей BTC (M15)
            btc_df = provider.fetch_candles(self.btc_symbol, '15m', 20)
            if btc_df is None or btc_df.empty:
                return 0, "NEUTRAL"

            last_close = btc_df['close'].iloc[-1]
            prev_close = btc_df['close'].iloc[-2]
            
            # 1. ДЕТЕКТОР КРАША (Защита от пролива)
            change_pct = (last_close - prev_close) / prev_close
            
            # Если BTC упал > 0.4% за 15 мин - ШТРАФУЕМ ВСЕ ЛОНГИ
            if change_pct < -0.004:
                return -15, "DANGER_DUMP" # Этот штраф «убьет» любой сигнал по альте
            
            # 2. ТРЕНД BTC (SMA 10)
            sma_10 = btc_df['close'].rolling(window=10).mean().iloc[-1]
            
            if last_close > sma_10:
                return 4, "BULLISH" # BTC помогает рынку растти
            else:
                return -4, "BEARISH" # BTC тянет рынок вниз
                
        except Exception as e:
            print(f"❌ Ошибка в CorrelationGuard: {e}")
            return 0, "ERROR"
