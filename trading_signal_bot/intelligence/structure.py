import pandas as pd

class StructureAnalyzer:
    def find_fvg(self, df):
        """
        Ищет свежий Imbalance (FVG) в последних 10 свечах.
        FVG — это разрыв между тенями 1-й и 3-й свечи в импульсе.
        """
        fvgs = []
        if len(df) < 5: return fvgs
        
        # Смотрим последние 10 свечей M15 (самый свежий след)
        limit = len(df) - 10
        for i in range(len(df) - 1, limit, -1):
            if i < 2: break
            
            # Bullish FVG (Бычий имбаланс: Low 3-й свечи выше High 1-й)
            if df['low'].iloc[i] > df['high'].iloc[i-2]:
                fvgs.append({
                    'type': 'bullish', 
                    'top': df['low'].iloc[i], 
                    'bottom': df['high'].iloc[i-2],
                    'size_pct': (df['low'].iloc[i] - df['high'].iloc[i-2]) / df['high'].iloc[i-2] * 100
                })
                
            # Bearish FVG (Медвежий имбаланс: High 3-й свечи ниже Low 1-й)
            elif df['high'].iloc[i] < df['low'].iloc[i-2]:
                fvgs.append({
                    'type': 'bearish', 
                    'top': df['low'].iloc[i-2], 
                    'bottom': df['high'].iloc[i],
                    'size_pct': (df['low'].iloc[i-2] - df['high'].iloc[i]) / df['high'].iloc[i] * 100
                })
        return fvgs

    def find_orderblock(self, df, side='buy'):
        """
        Ищет свежий Orderblock (последние 10 свечей).
        Это последняя манипулятивная свеча перед сломом структуры или сильным импульсом.
        """
        if len(df) < 15: return None
        lookback = 10 
        
        if side == 'buy':
            # Ищем последнюю медвежью свечу, которую поглотили вверх
            for i in range(len(df)-2, len(df)-lookback, -1):
                if df['close'].iloc[i] < df['open'].iloc[i]: # Медвежья
                    if df['close'].iloc[i+1] > df['high'].iloc[i]: # Поглощение
                        return {
                            'top': df['high'].iloc[i], 
                            'bottom': df['low'].iloc[i], 
                            'age': len(df)-i
                        }
        else:
            # Ищем последнюю бычью свечу, которую поглотили вниз
            for i in range(len(df)-2, len(df)-lookback, -1):
                if df['close'].iloc[i] > df['open'].iloc[i]: # Бычья
                    if df['close'].iloc[i+1] < df['low'].iloc[i]: # Поглощение
                        return {
                            'top': df['high'].iloc[i], 
                            'bottom': df['low'].iloc[i], 
                            'age': len(df)-i
                        }
        return None
