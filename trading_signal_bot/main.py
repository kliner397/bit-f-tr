import asyncio
import os
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

# Импорты из твоих папок
from data.provider import MarketProvider
from intelligence.intelligence import IntelligenceModule
from intelligence.market_regime import MarketRegime
from intelligence.structure import StructureAnalyzer
from intelligence.correlation import CorrelationGuard
from intelligence.whale_walls import WhaleWalls # Новый импорт
from execution.target_engine import TargetEngine
from delivery.telegram_bot import TelegramSignalBot

# --- НАСТРОЙКИ ---
TG_TOKEN = "8684560734:AAHFbQ7L6Eh7OOSsd8KeASkrzU60Ub0OosM"
CHAT_ID = 269901329  
THRESHOLD = 14      

class SignalEngine:
    def __init__(self):
        # Инициализация всех аналитических модулей
        self.provider = MarketProvider()
        self.targets = TargetEngine(precision=4)
        self.intel = IntelligenceModule(threshold=THRESHOLD)
        self.regime = MarketRegime()
        self.struct = StructureAnalyzer()
        self.guard = CorrelationGuard()
        self.walls = WhaleWalls() # Инициализируем детектор стенок
        
        # Настройка Telegram
        session = AiohttpSession()
        self.tg = TelegramSignalBot(TG_TOKEN, CHAT_ID)
        self.tg.bot = Bot(token=TG_TOKEN, session=session)

    async def run_cycle(self):
        # 1. ПРОВЕРКА БИТКОИНА (Предохранитель)
        print(f"\n🔍 Проверка состояния BTC...")
        btc_bonus, btc_status = self.guard.analyze_market_health(self.provider.exchange, self.provider)
        
        if btc_status == "DANGER_DUMP":
            print(f"⚠️ BTC КРАШИТСЯ! Скан заблокирован для безопасности.")
            return

        print(f"🚀 [SMC SCANNER] Анализ ТОП-150 пар (BTC: {btc_status})...")
        pairs = self.provider.get_top_pairs(150) 

        for symbol in pairs:
            if "BTC/USDT" in symbol: 
                continue

            # Загрузка данных свечей (H4, H1, M15)
            data = self.provider.get_mtf_data(symbol)
            if not data or any(v is None for v in data.values()): 
                continue

            # 2. БАЗОВЫЙ АНАЛИЗ (RSI, Тренд, OI)
            analysis = self.intel.analyze_market(data, self.provider.exchange, symbol)
            
            # 3. ДОБАВЛЯЕМ БОНУС БИТКОИНА
            analysis['score'] += btc_bonus
            
            # 4. АНАЛИЗ РЕЖИМА (Боковик/Тренд)
            regime_name, regime_score = self.regime.analyze(data['H1'])
            analysis['score'] += regime_score
            
            if regime_name == "FLAT": 
                continue

            # 5. ПОИСК ORDERBLOCK
            ob_zone = self.struct.find_orderblock(data['M15'], side=analysis['side'])
            if ob_zone: 
                analysis['score'] += 5 

            # 6. АНАЛИЗ СТЕНОК (Whale Walls)
            wall_bonus, wall_status = self.walls.analyze_orderbook(self.provider.exchange, symbol)
            
            # Начисляем бонус, если стенка подтверждает наше направление
            if analysis['side'] == 'buy' and wall_status == "BULL_WALL":
                analysis['score'] += 4
            elif analysis['side'] == 'sell' and wall_status == "BEAR_WALL":
                analysis['score'] += 4

            # ФИНАЛЬНАЯ ПРОВЕРКА ПОРОГА
            if analysis['score'] >= self.intel.threshold and analysis['side'] != 'none':
                # Расчет целей (адаптивный стоп и тейки по H4)
                targets = self.targets.calculate_smart_targets(
                    data, 
                    side=analysis['side'], 
                    ob_zone=ob_zone,
                    is_pump=analysis['is_pump']
                )
                
                # Пропускаем неактуальные сигналы или плохой RR
                if not targets or targets['rr'] < 1.5: 
                    continue

                print(f"✅ СИГНАЛ: {symbol} | СИЛА: {analysis['score']} | {regime_name}")
                
                try:
                    # Отправка в Telegram (с учетом статуса BTC)
                    await self.tg.send_signal(symbol, analysis, targets, btc_status=btc_status)
                except Exception as e:
                    print(f"❌ Ошибка ТГ: {e}")

            # Пауза для стабильности API
            await asyncio.sleep(0.6)

async def main():
    engine = SignalEngine()
    greeting = "🚀 Бот запущен и готов к отлову денег!"
    print(f"🤖 {greeting}")
    
    try:
        await engine.tg.bot.send_message(chat_id=CHAT_ID, text=greeting)
    except: 
        pass
    
    while True:
        try:
            await engine.run_cycle()
            print("\n⏳ Цикл завершен. Ожидание 5 минут...")
            await asyncio.sleep(300)
        except Exception as e:
            print(f"❌ Ошибка в главном цикле: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен.")
