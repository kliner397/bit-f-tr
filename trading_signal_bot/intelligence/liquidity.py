import pandas as pd

class LiquidityFinder:
    def find_pools(self, df):
        """Ищет пулы ликвидности (Equal Highs/Lows)"""
        pools = {'highs': [], 'lows': []}
        if len(df) < 50: return pools
        
        # Ищем "ровные" максимумы (сопротивление толпы)
        highs = df['high'].tail(50)
        for val in highs:
            # Если цена подходила к этому уровню несколько раз (разница < 0.1%)
            count = sum(1 for h in highs if abs(h - val) / val < 0.001)
            if count >= 2:
                if val not in pools['highs']: pools['highs'].append(val)
                
        # Ищем "ровные" минимумы (поддержка толпы)
        lows = df['low'].tail(50)
        for val in lows:
            count = sum(1 for l in lows if abs(l - val) / val < 0.001)
            if count >= 2:
                if val not in pools['lows']: pools['lows'].append(val)
        
        return pools

    def get_nearest_target(self, current_price, pools, side='buy'):
        """Находит ближайший пул ликвидности для тейка"""
        if side == 'buy':
            targets = [p for p in pools['highs'] if p > current_price]
            return min(targets) if targets else None
        else:
            targets = [p for p in pools['lows'] if p < current_price]
            return max(targets) if targets else None
