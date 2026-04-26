import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Profile
from database import init_db, add_user, get_user_name, update_user_name, add_expense
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
    update_user_name(message.from_user.id, message.text)
    await state.clear()
    await message.answer(f"Имя {message.text} сохранено!")
@dp.message()
async def handle_all(message: types.Message, state: FSMContext):
    if message.text == "Start":
        await message.answer("Погнали.")
    elif message.text.lower() == "info":
        await message.answer("Привет, это мой первый бот на пайтон")
    elif message.text.lower() == "settings":
        current_name = get_user_name(message.from_user.id)
        btn_name = KeyboardButton(text="Изменить имя")
        btn_back = KeyboardButton(text="Назад")
        settings_kb = ReplyKeyboardMarkup(keyboard=[[btn_name, btn_back]], resize_keyboard=True)
        await message.answer(f"Твое имя: {current_name}, Что изменим? ", reply_markup=settings_kb)
    elif message.text.lower() == "изменить имя":
        await state.set_state(Profile.name)
        await message.answer("Как тебя зовут?")
    elif message.text.lower() == "назад":
        await start(message)
    else:
        data = message.text.split()
        if len(data) == 2:
            try:
                category = data[0]
                summa = float(data[1])
                add_expense(message.from_user.id, summa, category)
                await message.answer("Сохранено")
            except ValueError:
                await message.answer("Сумму нужно вводить цифрами")
        else:
            await message.answer("Я тебя не понимаю. Введи расход (Еда 500) или нажми кнопку.")
async def main():
    init_db()
    await dp.start_polling(bot)
asyncio.run(main())