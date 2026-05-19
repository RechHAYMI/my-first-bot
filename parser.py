import asyncio
import httpx 
from bs4 import BeautifulSoup
from database import all_user_id
from main import bot



async def shadow_parser():
    current_quotes = await get_quotes()
    last_status = current_quotes[0]
    while True:
        print("Проверяю сайт...")
        new_quotes = await get_quotes()
        new_status = new_quotes[0]
        users = all_user_id()
        if new_status != last_status:
            for user in users:
                try:
                    await bot.send_message(chat_id=user[0], text=f"Новая цитата!\n\n{new_status}")
                    await asyncio.sleep(0.05)
                except Exception as e:
                    print(f"Не удалось отправить {user[0]}. Ошибка: {e}")
            last_status = new_status
    
        await asyncio.sleep(10)

async def get_quotes():
    results = []
    async with httpx.AsyncClient() as client:
        response = await client.get("https://quotes.toscrape.com/")
        soup = BeautifulSoup(response.text, "html.parser")
        authors = soup.find_all("small", class_="author")
        quotes = soup.find_all("span", class_="text")
        for quote, author in zip(quotes, authors):
            results.append(f"{quote.text} — {author.text}")
        return results