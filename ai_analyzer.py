
import os
import aiohttp

async def get_gemini_analysis(price, market_news, global_news, calendar):
    prompt = f"""
Anda adalah analis profesional untuk XAU/USD. Berdasarkan data berikut, buat analisa singkat dan jelas.

Harga & Bias Teknis:
{price}

Berita Finansial:
{market_news}

Berita Global:
{global_news}

Kalender Ekonomi:
{calendar}

Analisa:
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{url}?key={os.environ['GEMINI_API_KEY']}", headers=headers, json=body) as resp:
            data = await resp.json()
            return data['candidates'][0]['content']['parts'][0]['text']
