import pandas as pd

class WhaleTracker:
    def analyze_oi(self, symbol, exchange):
        """Анализ Открытого Интереса (OI)"""
        try:
            # Получаем данные OI через CCXT
            oi_data = exchange.fetch_open_interest(symbol)
            if not oi_data:
                return 0
            
            # Если по монете есть активный интерес - это хороший знак
            # (Для синхронной версии проверяем просто наличие данных)
            oi_value = float(oi_data['openInterestAmount'])
            
            if oi_value > 0:
                return 4  # +4 балла к Score за наличие интереса крупных игроков
            return 0
        except Exception as e:
            # Если биржа не отдает OI для этой пары - просто 0
            return 0

    def check_volume_surge(self, df_m15):
        """Проверка аномального объема (Следы китов)"""
        avg_vol = df_m15['volume'].tail(20).mean()
        last_vol = df_m15['volume'].iloc[-1]
        
        if last_vol > avg_vol * 4: # Если объем в 4 раза выше среднего
            return 3 # +3 балла за 'китовый' всплеск
        return 0
