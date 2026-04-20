import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Приветик! Это мой первый бот.")
@dp.message()
async def copy_message(message: types.Message):
    await message.answer(message.text)
async def main():
    await dp.start_polling(bot)
asyncio.run(main())