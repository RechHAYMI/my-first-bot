import asyncio
import os
import csv
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from utils import generate_stats_chart
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Profile
from database import init_db, add_user, get_user_name, update_user_name, add_expense, get_total_expenses, get_category_stats, delete_last_expense, get_all_expenses



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
    button_stats = KeyboardButton(text="Stats")
    button_cansel = KeyboardButton(text="Canсel")
    button_export = KeyboardButton(text="Export")
    my_kb = ReplyKeyboardMarkup(keyboard=[[button_start, button_info], [button_settings, button_stats], [button_cansel, button_export]], resize_keyboard=True)
    await message.answer("Привет! Нажми на кнопку ниже, чтобы начать.", reply_markup=my_kb)



@dp.message(Profile.name)
async def name(message: types.Message, state: FSMContext):
    update_user_name(message.from_user.id, message.text)
    await state.clear()
    await message.answer(f"Имя {message.text} сохранено!")



@dp.message()
async def handle_all(message: types.Message, state: FSMContext):
    if message.text.lower() == "start":
        await message.answer("Погнали.")
    elif message.text.lower() == "info":
        await message.answer("Привет, это мой первый бот на пайтон")
    elif message.text.lower() == "stats":
        rows = get_category_stats(message.from_user.id)
        if not rows:
            await message.answer("У вас еще нету данных для статистики")
            return
        else:
            photo_name = generate_stats_chart(rows, message.from_user.id)
            await message.answer_photo(photo=FSInputFile(photo_name))
            os.remove(photo_name)
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
    elif message.text.lower() == "canсel":
        delete_last_expense(message.from_user.id)
        await message.answer("Последния операция была отменена")
    elif message.text.lower() == "export":
        rows = get_all_expenses(message.from_user.id)
        if not rows:
            await message.answer("У вас пока нет данных для экспорта.")
            return
        filename = f"report_{message.from_user.id}.csv"
        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Категория", "Сумма", "Дата"])
            writer.writerows(rows)
        file_to_send = FSInputFile(filename)
        await message.answer_document(file_to_send, caption="Ваш отчет готов!")
        os.remove(filename)
    else:
        data = message.text.split()
        if len(data) == 2:
            try:
                category = data[0].lower().capitalize()
                clean_summa = data[1].replace(",", ".")
                summa = float(clean_summa)
                if len(category) > 20:
                    await message.answer("Название слишком длинное (max 20 симв.)")
                else:
                    if summa > 0 and summa < 100000:
                        add_expense(message.from_user.id, summa, category)
                        await message.answer("Сохранено")
                    else:
                        await message.answer("Ошибка, сумма должна быть больше нуля и меньше 100000.")
            except ValueError:
                await message.answer("Сумму нужно вводить цифрами")
        else:
            await message.answer("Я тебя не понимаю. Введи расход (Еда 500) или нажми кнопку.")



async def main():
    init_db()
    await dp.start_polling(bot)



asyncio.run(main())