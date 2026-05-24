import asyncio
import httpx
from bs4 import BeautifulSoup

async def test_parser():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            response = await client.get("https://quotes.toscrape.com/")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                authors = soup.find_all("small", class_="author")
                quotes = soup.find_all("span", class_="text")
                
                if not quotes or not authors:
                    print("Внимание: Вёрстка сайта изменилась или данные не найдены!")
                else:
                    for quote, author in zip(quotes, authors):
                        print(f"{quote.text} — {author.text}")
            else:
                print(f"Сервер ответил странным статусом: {response.status_code}")
                
        except httpx.HTTPError as e:
            print(f"Произошла сетевая ошибка при запросе: {e}")

if __name__ == "__main__":
    asyncio.run(test_parser())