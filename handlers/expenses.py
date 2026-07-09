import logging
import os
import csv
import matplotlib.pyplot as plt

from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.filters import Command


from keyboards import get_main_kb, get_categor_kb, get_delete_kb, CategoryCallback
from states import Profile, FSMExpense, Broadcast
from utils import generate_stats_chart



router = Router()


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log", encoding="utf-8")
logger = logging.getLogger(__name__)


@router.message(F.text.lower() == "add expenses")
@router.message(Command("add_expenses"))
async def add_expense(message: types.Message, state: FSMContext):
    await state.set_state(FSMExpense.categor)
    await message.answer("Выберите категорию ниже", reply_markup=get_categor_kb())


@router.callback_query(CategoryCallback.filter())
async def categor(callback: types.CallbackQuery, callback_data: CategoryCallback, state: FSMContext):
    category_name = callback_data.name
    await state.update_data(categor=category_name)
    await state.set_state(FSMExpense.sum)
    await callback.message.answer(f"Выбрана категория: {category_name}. Теперь введите сумму.")
    await callback.answer()



@router.message(FSMExpense.sum)
async def process_sum(message: types.Message, state: FSMContext, db):
    user_data = await state.get_data()
    category = user_data.get("categor")
    try:
        amount = float(message.text.replace(",", "."))
        await db.add_expense(message.from_user.id, amount, category)
        await state.clear()
        await message.answer(f"Записано: {amount} руб. в категорию {category}")
    except ValueError:
        await message.answer("Ошибка! Введи сумму цифрами (например, 500 или 150.50)")


@router.message(F.text.lower() == "stats")
@router.message(Command("stats"))
async def stats(message: types.Message, db):
    rows = await db.get_category_stats(message.from_user.id)
    if not rows:
        await message.answer("У вас еще нету данных для статистики")
        return
    else:
        photo_name = generate_stats_chart(rows, message.from_user.id)
        await message.answer_photo(photo=FSInputFile(photo_name))
        os.remove(photo_name)



@router.callback_query(F.data == "delete_exp")
async def delete_callback(callback: types.CallbackQuery, db):
    logger.info(f"Пользователь {callback.from_user.id} удалил свой последний расход")
    await db.delete_last_expense(callback.from_user.id)
    await callback.answer("Расход удален!")
    await callback.message.edit_text("Запись успешно удалена!")



@router.message(F.text.lower() == "export")
@router.message(Command("export"))
async def export(message: types.Message, db):
    rows = await db.get_all_expenses(message.from_user.id)
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