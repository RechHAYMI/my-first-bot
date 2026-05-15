import logging
import os
import csv
import matplotlib.pyplot as plt
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards import get_main_kb, get_categor_kb, get_delete_kb
from states import Profile, FSMExpense, Broadcast
from database import get_category_stats, delete_last_expense, db_add_expense
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from utils import generate_stats_chart



router = Router()


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log", encoding="utf-8")
logger = logging.getLogger(__name__)


@router.message(F.text.lower() == "add expenses")
@router.message(Command("add expenses"))
async def add_expense(message: types.Message, state: FSMContext):
    await state.set_state(FSMExpense.categor)
    await message.answer("Выберите категорию ниже", reply_markup=get_categor_kb())


@router.callback_query(F.data.startswith("cat_"))
async def categor(callback: types.CallbackQuery, state: FSMContext):
    category_name = callback.data.split("_")[1]
    await state.update_data(categor=category_name)
    await state.set_state(FSMExpense.sum)
    await callback.message.answer(f"Выбрана категория: {category_name}. Теперь введите сумму.")
    await callback.answer()



@router.message(FSMExpense.sum)
async def process_sum(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    category = user_data.get("categor")
    try:
        amount = float(message.text.replace(",", "."))
        db_add_expense(message.from_user.id, amount, category)
        await state.clear()
        await message.answer(f"Записано: {amount} руб. в категорию {category}")
    except ValueError:
        await message.answer("Ошибка! Введи сумму цифрами (например, 500 или 150.50)")


@router.message(F.text.lower() == "stats")
@router.message(Command("stats"))
async def stats(message: types.Message):
    rows = get_category_stats(message.from_user.id)
    if not rows:
        await message.answer("У вас еще нету данных для статистики")
        return
    else:
        photo_name = generate_stats_chart(rows, message.from_user.id)
        await message.answer_photo(photo=FSInputFile(photo_name))
        os.remove(photo_name)



@router.message(F.text.lower() == "cancel")
@router.message(Command("cancel"))
async def cansel(message: types.Message):
    delete_last_expense(message.from_user.id)
    await message.answer("Последния операция была отменена")


@router.callback_query(F.data == "delete_exp")
async def delete_callback(callback: types.CallbackQuery):
    logger.info(f"Пользователь {callback.from_user.id} удалил свой последний расход")
    delete_last_expense(callback.from_user.id)
    await callback.answer("Расход удален!")
    await callback.message.edit_text("Запись успешно удалена!")



@router.message(F.text.lower() == "export")
@router.message(Command("export"))
async def export(message: types.Message):
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