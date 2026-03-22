import pandas as pd
import numpy as np

class MarketRegime:
    def get_adx(self, df, period=14):
        """Расчет силы тренда ADX (без сторонних библиотек)"""
        df = df.copy()
        df['up'] = df['high'].diff()
        df['down'] = df['low'].diff().abs()
        
        df['+dm'] = np.where((df['up'] > df['down']) & (df['up'] > 0), df['up'], 0)
        df['-dm'] = np.where((df['down'] > df['up']) & (df['down'] > 0), df['down'], 0)
        
        tr = pd.concat([df['high'] - df['low'], 
                        (df['high'] - df['close'].shift()).abs(), 
                        (df['low'] - df['close'].shift()).abs()], axis=1).max(axis=1)
        
        atr = tr.rolling(window=period).mean()
        p_di = 100 * (df['+dm'].rolling(window=period).mean() / atr)
        m_di = 100 * (df['-dm'].rolling(window=period).mean() / atr)
        
        dx = 100 * (p_di - m_di).abs() / (p_di + m_di)
        return dx.rolling(window=period).mean().iloc[-1]

    def analyze(self, df_h1):
        """Определяет режим рынка: TRENDING (тренд) или FLAT (боковик)"""
        try:
            adx_value = self.get_adx(df_h1)
            
            if adx_value < 20:
                return "FLAT", 0      # Боковик: 0 баллов (сигнал вряд ли пройдет)
            elif adx_value > 25:
                return "TRENDING", 4  # Сильный тренд: +4 балла к Score
            return "NORMAL", 2        # Обычный рынок: +2 балла
        except:
            return "UNKNOWN", 0
