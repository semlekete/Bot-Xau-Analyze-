
import asyncio
from finnhub_client import get_market_news

def start_news_watcher(app, analysis_func, registered_chats):
    async def watch_news():
        last_headline = ""
        while True:
            news = await get_market_news()
            if news and news != last_headline:
                last_headline = news
                analysis = await analysis_func()
                for chat_id in registered_chats:
                    try:
                        await app.bot.send_message(chat_id=chat_id, text=analysis)
                    except Exception as e:
                        print(f"Gagal kirim breaking news ke {chat_id}: {e}")
            await asyncio.sleep(600)
    asyncio.create_task(watch_news())
