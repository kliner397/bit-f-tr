import aiohttp
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

class TelegramSignalBot:
    def __init__(self, token, chat_id):
        session = AiohttpSession()
        self.bot = Bot(token=token, session=session)
        self.chat_id = chat_id
        # Устанавливаем теоретический максимум для шкалы
        self.max_score = 33 

    def generate_progress_bar(self, score):
        """Рисует визуальную шкалу силы сигнала"""
        percent = min(int((score / self.max_score) * 100), 100)
        filled_length = int(10 * percent // 100)
        bar = "🟩" * filled_length + "⬜" * (10 - filled_length)
        return f"{bar} {percent}%"

    async def send_signal(self, symbol, intel, targets, btc_status="NEUTRAL"):
        """Отправка сигнала с прогресс-баром"""
        clean_symbol = symbol.split(':')[0]
        side_emoji = "🚀 **LONG**" if intel['side'] == 'buy' else "📉 **SHORT**"
        btc_emoji = "🟢" if btc_status == "BULLISH" else "🔴" if btc_status == "BEARISH" else "🟡"
        
        # Генерируем шкалу
        progress_bar = self.generate_progress_bar(intel['score'])

        message = (
            f"💎 **СИГНАЛ: {clean_symbol}**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔥 СИЛА: **{intel['score']}** / {self.max_score}\n"
            f"📊 {progress_bar}\n\n"
            f"🎯 СТАТУС: {side_emoji}\n"
            f"{btc_emoji} РЫНОК (BTC): **{btc_status}**\n"
            f"⚙️ РЕЖИМ: **{targets.get('mode', 'N/A')}**\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"📍 **ЗОНА ВХОДА:**\n`{targets['entry_zone']}`\n\n"
            f"🚫 **СТОП-ЛОСС:**\n`{targets['sl']}`\n\n"
            f"🎯 **ЦЕЛИ (TP):**\n"
            f"1️⃣ `{targets['tp1']}`\n"
            f"2️⃣ `{targets['tp2']}`\n"
            f"3️⃣ `{targets['tp3']}`\n\n"
            f"📈 *Risk/Reward: 1:{targets['rr']}*"
        )
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id, 
                text=message, 
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ Ошибка ТГ: {e}")
