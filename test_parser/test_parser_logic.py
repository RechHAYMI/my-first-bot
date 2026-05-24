import pytest
import asyncio
import httpx
from bs4 import BeautifulSoup


@pytest.mark.asyncio
async def test_quotes_website_structure():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get("https://quotes.toscrape.com/")
        assert response.status_code == 200
        soup = BeautifulSoup(response.text, "html.parser")
        authors = soup.find_all("small", class_="author")
        quotes = soup.find_all("span", class_="text")

        assert len(quotes) > 0

        assert len(quotes) == len(authors)

        print("\nТест пройден успешно!")