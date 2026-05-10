import asyncio
import os
import csv
import matplotlib.pyplot as plt
import logging
from dotenv import load_dotenv
from utils import generate_stats_chart
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from states import Profile, FSMExpense
from middlewares.db_check import DbCheckMiddleware
from keyboards import get_main_kb, get_delete_kb, get_settings_kb
from database import init_db, add_user, get_user_name, update_user_name, add_expense, get_total_expenses, get_category_stats, delete_last_expense, get_all_expenses



load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log", encoding="utf-8")
logger = logging.getLogger(__name__)



bot = Bot(token=TOKEN)

dp = Dispatcher()


dp.message.outer_middleware(DbCheckMiddleware())
dp.callback_query.outer_middleware(DbCheckMiddleware())


@dp.message(Command("start"))
async def start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} зарегистрировался.")
    await message.answer("Привет!", reply_markup=get_main_kb())



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
        await message.answer(f"Твое имя: {current_name}, Что изменим? ", reply_markup=get_settings_kb())
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
        logger.info(f"Пользователь {message.from_user.id} экспортировал свои данные.")
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
    elif message.text.lower() == "добавить расход":
        await state.set_state(FSMExpense.categor)
        await message.answer("Выберите категорию ниже", reply_markup=get_categor_kb())
        get_categor_kb(callback.from_user.id)


@dp.callback_query(F.data == "delete_exp")
async def delete_callback(callback: types.CallbackQuery):
    logger.info(f"Пользователь {callback.from_user.id} удалил свой последний расход")
    delete_last_expense(callback.from_user.id)
    await callback.answer("Расход удален!")
    await callback.message.edit_text("Запись успешно удалена!")


@dp.callback_query(F.data.startswith("cat_"))
async def categor(callback: types.CallbackQuery, state: FSMContext):
    category_name = callback.data.split("_")[1]
    await state.update_data(categor=category_name)
    await state.set_state(FSMExpense.SUM)
    await callback.message.answer(f"Выбрана категория: {category_name}. Теперь введите сумму.")
    await callback.answer()



@dp.message(FSMExpense.sum)
async def process_sum(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    category = user_data.get("categor")
    try:
        amount = float(message.text.replace(",", "."))
        add_expense(message.from_user.id, amount, category)
        await state.clear()
        await message.answer(f"Записано: {amount} руб. в категорию {category}")
    except ValueError:
        await message.answer("Ошибка! Введи сумму цифрами (например, 500 или 150.50)")


async def main():
    init_db()
    logger.info("Бот запущен и готов к работе")
    await dp.start_polling(bot)


asyncio.run(main())