import pandas as pd

class WhaleWalls:
    def __init__(self, imbalance_threshold=2.0):
        self.threshold = imbalance_threshold # Во сколько раз покупателей больше продавцов

    def analyze_orderbook(self, exchange, symbol):
        """Ищет крупные стенки в стакане (Order Book)"""
        try:
            # Берем стакан глубиной 50 (хватит для анализа ближайших уровней)
            ob = exchange.fetch_order_book(symbol, limit=50)
            
            # Считаем сумму 10 лучших заявок на покупку и продажу
            bids_vol = sum([bid[1] for bid in ob['bids'][:10]])
            asks_vol = sum([ask[1] for ask in ob['asks'][:10]])
            
            if asks_vol == 0: return 0, "NEUTRAL"
            
            imbalance = bids_vol / asks_vol
            
            # Если покупателей в 2 раза больше (стенка снизу)
            if imbalance >= self.threshold:
                return 4, "BULL_WALL" # +4 балла к Score
            # Если продавцов в 2 раза больше (стенка сверху)
            elif imbalance <= (1 / self.threshold):
                return -4, "BEAR_WALL" # Штраф или баллы для SHORT
            
            return 0, "BALANCED"
        except Exception as e:
            # Если биржа не отдает стакан (редко)
            return 0, "NO_DATA"
