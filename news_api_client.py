
import aiohttp
import os

async def get_global_news():
    url = f"https://newsapi.org/v2/top-headlines?language=en&q=geopolitic&apiKey={os.environ['NEWSAPI_API_KEY']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            news = await resp.json()
            top = news["articles"][:3]
            return "\n".join([f"- {n['title']}" for n in top])
