import pandas as pd
import numpy as np

class IntelligenceModule:
    def __init__(self, threshold=11):
        self.threshold = threshold

    def calculate_rsi(self, series, period=14):
        """Чистый расчет RSI"""
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (100 + rs))

    def analyze_market(self, data_mtf, exchange, symbol):
        """Основной мозг: считает баллы на основе RSI, Тренда и КИТОВ (OI)"""
        df_h1 = data_mtf['H1'].copy()
        df_m15 = data_mtf['M15'].copy()
        
        score = 0
        side = 'none'
        
        # --- 1. ТРЕНД (EMA 200) на H1 ---
        ema_200 = df_h1['close'].ewm(span=200, adjust=False).mean()
        last_close = df_h1['close'].iloc[-1]
        trend_up = last_close > ema_200.iloc[-1]
        score += 4 if trend_up else 0
        
        # --- 2. RSI (14) на M15 ---
        rsi_series = self.calculate_rsi(df_m15['close'])
        last_rsi = rsi_series.iloc[-1]
        if last_rsi < 35: score += 4
        elif last_rsi > 65: score += 4

        # --- 3. ПАМП / ДАМП (Объем) ---
        avg_vol = df_m15['volume'].tail(20).mean()
        last_vol = df_m15['volume'].iloc[-1]
        is_pump = last_vol > (avg_vol * 3)
        if is_pump: score += 5
            
        # --- 4. КИТЫ: OPEN INTEREST (OI) ---
        # Если в монету вливают деньги - это подтверждение китов
        whale_score = 0
        try:
            oi_data = exchange.fetch_open_interest(symbol)
            if oi_data and float(oi_data['openInterestAmount']) > 0:
                whale_score = 3 # +3 балла за активность китов
        except:
            pass
        score += whale_score

        # Определяем направление
        if score >= 3: # Предварительный расчет стороны сделки
            side = 'buy' if (trend_up or last_rsi < 35) else 'sell'
                
        return {
            'score': score, 
            'side': side, 
            'is_pump': is_pump, 
            'rsi': round(last_rsi, 2),
            'whale_signal': whale_score > 0
        }
