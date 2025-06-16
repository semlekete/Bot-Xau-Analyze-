
import aiohttp
import os

async def get_price_analysis():
    url = f"https://finnhub.io/api/v1/quote?symbol=XAUUSD&token={os.environ['FINNHUB_API_KEY']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return f"Harga Sekarang: ${data['c']}"

async def get_market_news():
    url = f"https://finnhub.io/api/v1/news?category=forex&token={os.environ['FINNHUB_API_KEY']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            news = await resp.json()
            top = news[:3]
            return "\n".join([f"- {n['headline']}" for n in top])

async def get_economic_events():
    url = f"https://finnhub.io/api/v1/calendar/economic?token={os.environ['FINNHUB_API_KEY']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            events = [e for e in data.get("economicCalendar", []) if e["impact"] in ["medium", "high"] and e["currency"] in ["USD", "EUR", "CNY", "JPY"]]
            return "\n".join([f"{e['time']} - {e['event']} ({e['currency']})" for e in events[:3]])
