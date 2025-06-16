
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import keep_alive
from ai_analyzer import get_gemini_analysis
from finnhub_client import get_price_analysis, get_market_news, get_economic_events
from news_api_client import get_global_news
from news_watcher import start_news_watcher
import os

logging.basicConfig(level=logging.INFO)

# In-memory database of registered chat IDs
registered_chats = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Selamat datang! Gunakan /analyze untuk analisa pasar dan /register untuk menerima update harian.")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Menganalisa pasar...")
    result = await send_daily_analysis()
    await update.message.reply_text(result)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    registered_chats.add(chat_id)
    await update.message.reply_text("✅ Berhasil mendaftar untuk menerima analisa otomatis setiap pagi.")

async def send_daily_analysis():
    tasks = [
        get_price_analysis(),
        get_market_news(),
        get_global_news(),
        get_economic_events()
    ]
    price, market_news, global_news, calendar = await asyncio.gather(*tasks)
    analysis = await get_gemini_analysis(price, market_news, global_news, calendar)

    return f"📈 Harga & Bias:
{price}

📰 Berita Terkini:
{market_news}

🌍 Berita Global:
{global_news}

📅 Kalender Ekonomi:
{calendar}

🤖 Analisa AI:
{analysis}"

async def scheduled_job(app):
    while True:
        from datetime import datetime, timedelta
        now = datetime.utcnow() + timedelta(hours=9)
        if now.hour == 7 and now.minute == 0:
            for chat_id in registered_chats:
                try:
                    result = await send_daily_analysis()
                    await app.bot.send_message(chat_id=chat_id, text=result)
                except Exception as e:
                    print(f"Gagal kirim ke {chat_id}: {e}")
        await asyncio.sleep(60)

async def main():
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(CommandHandler("register", register))

    keep_alive()
    start_news_watcher(app, send_daily_analysis, registered_chats)

    asyncio.create_task(scheduled_job(app))
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
