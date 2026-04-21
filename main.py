import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, ReplyKeyboardMarkup, KeyboardButton 
from aiogram.filters import Command
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
@dp.message(Command("start"))
async def start(message: types.Message):
    my_button = KeyboardButton(text="Start")
    my_kb = ReplyKeyboardMarkup(keyboard=[[my_button]], resize_keyboard=True)
    await message.answer("Приветик! Это мой первый бот.", reply_markup=my_kb)
@dp.message()
async def copy_message(message: types.Message):
    await message.answer(message.text)
async def main():
    await dp.start_polling(bot)
asyncio.run(main())