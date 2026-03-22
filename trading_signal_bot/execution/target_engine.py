import pandas as pd
from intelligence.liquidity import LiquidityFinder # Импортируем новый модуль

class TargetEngine:
    def __init__(self, precision=4):
        self.precision = precision
        self.liq = LiquidityFinder() # Инициализируем поиск ликвидности

    def calculate_smart_targets(self, data_mtf, side, ob_zone, is_pump=False):
        """
        Расчет целей по пулам ликвидности и адаптивных стопов.
        """
        df_m15 = data_mtf['M15']
        df_h1 = data_mtf['H1']
        df_h4 = data_mtf['H4']
        current_price = df_m15['close'].iloc[-1]
        
        if not ob_zone: 
            return None
        
        # 1. ЗОНА ВХОДА (Orderblock M15)
        entry_start = ob_zone['top']
        entry_end = ob_zone['bottom']

        # Проверка актуальности (дистанция до зоны не более 0.4%)
        dist_to_zone = abs(current_price - entry_start) / current_price
        if dist_to_zone > 0.004: 
            return None

        # 2. АДАПТИВНЫЙ СТОП-ЛОСС
        if is_pump:
            # Режим Импульса: короткий стоп за 3 свечи M15
            if side == 'buy':
                sl = df_m15['low'].tail(3).min() * 0.9995
            else:
                sl = df_m15['high'].tail(3).max() * 1.0005
        else:
            # Режим Структуры: надежный стоп за свинг H1 (18 свечей)
            if side == 'buy':
                swing_low = df_h1['low'].tail(18).min()
                sl = swing_low * 0.9985
            else:
                swing_high = df_h1['high'].tail(18).max()
                sl = swing_high * 1.0015

        # 3. ТЕЙК-ПРОФИТЫ (Поиск пулов ликвидности на H4)
        pools = self.liq.find_pools(df_h4)
        main_target = self.liq.get_nearest_target(current_price, pools, side)
        
        if main_target:
            # Если нашли реальный пул (Equal Highs/Lows) - ставим Тейки туда
            tp1 = current_price + (main_target - current_price) * 0.5 if side == 'buy' else current_price - (current_price - main_target) * 0.5
            tp2 = main_target
            tp3 = main_target * (1.015 if side == 'buy' else 0.985)
        else:
            # Если пулов нет - используем классические хаи/лои H4 (60 свечей)
            h4_ext = df_h4['high'].tail(60).max() if side == 'buy' else df_h4['low'].tail(60).min()
            tp1 = current_price + (h4_ext - current_price) * 0.4 if side == 'buy' else current_price - (current_price - h4_ext) * 0.4
            tp2 = h4_ext
            tp3 = h4_ext * (1.02 if side == 'buy' else 0.98)

        f = lambda x: f"{float(x):.{self.precision}f}"
        
        # Расчет Risk/Reward до основной цели TP2
        risk = abs(current_price - sl)
        reward = abs(float(tp2) - current_price)
        rr = round(reward / risk, 2) if risk > 0 else 0
        
        # Фильтр минимального качества сделки
        if rr < 1.5: 
            return None

        return {
            'entry_zone': f"{f(entry_start)} — {f(entry_end)}",
            'sl': f(sl),
            'tp1': f(tp1),
            'tp2': f(tp2),
            'tp3': f(tp3),
            'rr': rr,
            'mode': "🚀 IMPULSE" if is_pump else "📈 STRUCTURE"
        }
