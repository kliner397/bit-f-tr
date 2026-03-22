import ccxt
import pandas as pd
import time

class MarketProvider:
    def __init__(self):
        # Синхронная версия Bybit через зеркало
        self.exchange = ccxt.bybit({
            'enableRateLimit': True,
            'options': {'defaultType': 'linear'}
        })
        self.exchange.urls['api']['public'] = 'https://api.bytick.com'

    def get_top_pairs(self, limit=100):
        """Получает ТОП-100 пар по объему за 24 часа"""
        try:
            tickers = self.exchange.fetch_tickers()
            usdt_pairs = [s for s in tickers.keys() if s.endswith(':USDT')]
            # Сортируем по объему (quoteVolume)
            sorted_pairs = sorted(
                usdt_pairs, 
                key=lambda x: tickers[x].get('quoteVolume', 0), 
                reverse=True
            )
            return sorted_pairs[:limit]
        except Exception as e:
            print(f"❌ Ошибка получения пар: {e}")
            return []

    def fetch_candles(self, symbol, timeframe='1h', limit=100):
        """Загружает свечи с защитой от Rate Limit"""
        try:
            # Добавляем микро-паузу перед каждым запросом (0.2 сек)
            time.sleep(0.2) 
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            if not ohlcv: 
                return None
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Принудительно делаем числа числами для точности
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
                
            return df
        except Exception as e:
            if "10006" in str(e):
                print(f"⏳ Bybit просит подождать (Rate Limit)...")
                time.sleep(2)  # Пауза при перегрузке
            else:
                print(f"❌ Ошибка загрузки {symbol} ({timeframe}): {e}")
            return None

    def get_mtf_data(self, symbol):
        """Собирает данные сразу по 3 таймфреймам для анализа"""
        return {
            'H4': self.fetch_candles(symbol, '4h', 100),
            'H1': self.fetch_candles(symbol, '1h', 100),
            'M15': self.fetch_candles(symbol, '15m', 100)
        }

if __name__ == "__main__":
    provider = MarketProvider()
    print("🔍 Сканирую рынок...")
    top_pairs = provider.get_top_pairs(1)
    
    if top_pairs:
        top_1 = top_pairs[0]
        print(f"✅ Выбрана пара: {top_1}")
        
        data = provider.get_mtf_data(top_1)
        if data['M15'] is not None:
            price = data['M15']['close'].iloc[-1]
            print(f"📊 Данные H4, H1, M15 получены. Текущая цена: {price:.4f}")
    else:
        print("❌ Не удалось получить список пар.")
