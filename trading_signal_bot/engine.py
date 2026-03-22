from data.provider import MarketProvider
from intelligence.intelligence import IntelligenceModule
from execution.target_engine import TargetEngine
from delivery.telegram_bot import TelegramSignalBot


class SignalEngine:
    def __init__(self, threshold=11):
        self.provider = MarketProvider()
        self.targets = TargetEngine(precision=4)
        self.intel = IntelligenceModule(threshold=threshold)
        self.is_running = True

    async def run_cycle(self):
        print("\n🚀 [НОВЫЙ ЦИКЛ СКАНЕРA]")
        
        # 1. Получаем ТОП-100 пар
        pairs = self.provider.get_top_pairs(100)
        print(f"📡 Сканирую {len(pairs)} пар на Bybit...")

        for symbol in pairs:
            # 2. Грузим данные (H4, H1, M15)
            data = self.provider.get_mtf_data(symbol)
            
            if data['M15'] is None or data['M15'].empty:
                continue

            # 3. Анализируем сигнал (Score 11-20)
            analysis = self.intel.analyze_market(data)
            
            # Если сигнал прошел порог
            if analysis['score'] >= self.intel.threshold and analysis['side'] != 'none':
                # 4. Рассчитываем цели
                targets = self.targets.calculate_targets(data, side=analysis['side'])
                
                # ВЫВОД СИГНАЛА
                self.print_signal(symbol, analysis, targets)

            # Небольшая пауза, чтобы не спамить запросами к бирже
            await asyncio.sleep(0.1)

    def print_signal(self, symbol, intel, targets):
        """Форматированный вывод сигнала в консоль"""
        side_str = "🚀 LONG" if intel['side'] == 'buy' else "📉 SHORT"
        print(f"\n🔥 СИГНАЛ: {symbol}")
        print(f"📊 СИЛА: {intel['score']}/20")
        print(f"🎯 СТАТУС: {side_str}")
        print(f"📍 ЗОНА ВХОДА: {targets['entry_zone']}")
        print(f"🚫 СТОП-ЛОСС: {targets['sl']}")
        print(f"✅ TP1: {targets['tp1']} | TP2: {targets['tp2']} | TP3: {targets['tp3']}")
        print(f"📈 Risk/Reward: 1:{targets['rr']}")
        print("-" * 30)

async def main():
    # Создаем движок. Можешь поставить threshold=11 для реальности
    # Или оставить 3-5 для проверки, что всё работает
    engine = SignalEngine(threshold=5) 
    
    while engine.is_running:
        try:
            await engine.run_cycle()
            print("\n⏳ Ожидаю 5 минут до следующего сканирования...")
            await asyncio.sleep(300) # Пауза 5 минут между циклами
        except KeyboardInterrupt:
            engine.is_running = False
            print("🛑 Бот остановлен.")
        except Exception as e:
            print(f"❌ Ошибка цикла: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
