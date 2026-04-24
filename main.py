import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Profile
from database import init_db, add_user
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
@dp.message(Command("start"))
async def start(message: types.Message):
    add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    button_start = KeyboardButton(text="Start")
    button_info = KeyboardButton(text="Info")
    button_settings = KeyboardButton(text="Settings")
    my_kb = ReplyKeyboardMarkup(keyboard=[[button_start, button_info], [button_settings]], resize_keyboard=True)
    await message.answer("Привет! Нажми на кнопку ниже, чтобы начать.", reply_markup=my_kb)
@dp.message(Profile.name)
async def name(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Имя {message.text} сохранено!")
@dp.message()
async def handle_all(message: types.Message, state: FSMContext):
    if message.text == "Start":
        await message.answer("Погнали.")
    elif message.text.lower() == "info":
        await message.answer("Привет, это мой первый бот на пайтон")
    elif message.text.lower() == "settings":
        btn_name = KeyboardButton(text="Изменить имя")
        btn_back = KeyboardButton(text="Назад")
        settings_kb = ReplyKeyboardMarkup(keyboard=[[btn_name, btn_back]], resize_keyboard=True)
        await message.answer("Вы в настройках что изменим?", reply_markup=settings_kb)
    elif message.text.lower() == "изменить имя":
        await state.set_state(Profile.name)
        await message.answer("Как тебя зовут?")
    elif message.text.lower() == "назад":
        await start(message)
    else:
        await message.answer("Я тебя не понимаю.")
async def main():
    init_db()
    await dp.start_polling(bot)
asyncio.run(main())