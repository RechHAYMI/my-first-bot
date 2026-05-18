import asyncio
import httpx
from bs4 import BeautifulSoup



async def test_parser():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://quotes.toscrape.com/")
        soup = BeautifulSoup(response.text, "html.parser")
        authors = soup.find_all("small", class_="author")
        quotes = soup.find_all("span", class_="text")
        for quote, author in zip(quotes, authors):
            print(f"{quote.text} — {author.text}")

asyncio.run(test_parser())