import logging
import os
import csv

from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.filters import Command

from keyboards import get_main_kb, get_categor_kb, get_delete_kb, get_settings_kb, get_delete_category_kb, CategoryCallback, DeleteCategoryCallback
from states import Profile, FSMExpense, Broadcast
from utils import generate_stats_chart

router = Router()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log", encoding="utf-8")
logger = logging.getLogger(__name__)



@router.message(F.text.lower().in_({"add expenses 💸", "add expenses"}))
@router.message(Command("add_expenses"))
async def add_expense(message: types.Message, state: FSMContext, db):
    user_categories = await db.get_user_categories(message.from_user.id)
    await state.set_state(FSMExpense.categor)
    await message.answer("Выберите категорию ниже", reply_markup=get_categor_kb(user_categories))



@router.callback_query(CategoryCallback.filter())
async def categor(callback: types.CallbackQuery, callback_data: CategoryCallback, state: FSMContext):
    await callback.answer()
    category_name = callback_data.name
    if category_name == "+ new categories":
        await state.set_state(FSMExpense.waiting_for_custom_categories)
        await callback.message.answer("Введите название новой категории (не больше 50 символов).")
    else:
        await state.update_data(categor=category_name)
        await state.set_state(FSMExpense.sum)
        await callback.message.answer(f"Выбрана категория: {category_name}. Теперь введите сумму.")



@router.message(FSMExpense.waiting_for_custom_categories)
async def new_categories(message: types.Message, state: FSMContext, db):
    new_category = message.text.strip()
    if len(new_category) > 50:
        new_category = new_category[:50]
    await db.add_custom_category(message.from_user.id, new_category)
    await state.clear()
    await message.answer(f"Категория '{new_category}' успешно создана! Теперь вы можете выбрать её при добавлении расхода.", reply_markup=get_main_kb())



@router.callback_query(F.data == "open_delete_menu")
async def manage_categories_to_delete(callback: types.CallbackQuery, db):
    await callback.answer()
    user_categories = await db.get_user_categories(callback.from_user.id)
    if not user_categories:
        await callback.message.answer("У вас нет созданных кастомных категорий.")
        return
    await callback.message.edit_text(
        "Выберите категорию для удаления:", 
        reply_markup=get_delete_category_kb(user_categories)
    )



@router.callback_query(DeleteCategoryCallback.filter())
async def delete_category(callback: types.CallbackQuery, callback_data: DeleteCategoryCallback, db):
    await callback.answer("Удалено!")
    id_category = callback_data.id
    await db.delete_custom_category(id_category, callback.from_user.id)
    await callback.message.edit_text("Категория успешно удалена!")



@router.callback_query(F.data == "cancel_deletion")
async def cancel_category_deletion(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Удаление отменено.")



@router.message(FSMExpense.sum)
async def process_sum(message: types.Message, state: FSMContext, db):
    user_data = await state.get_data()
    category = user_data.get("categor")
    try:
        amount = float(message.text.replace(",", "."))
        await db.add_expense(message.from_user.id, amount, category)
        await state.clear()
        await message.answer(f"Записано: {amount} руб. в категорию {category}", reply_markup=get_delete_kb())
    except ValueError:
        await message.answer("Ошибка! Введи сумму цифрами (например, 500 или 150.50)")



@router.message(F.text.lower().in_({"stats 📊", "stats", "статистика"}))
@router.message(Command("stats"))
async def stats(message: types.Message, db):
    rows = await db.get_category_stats(message.from_user.id)
    if not rows:
        await message.answer("У вас еще нету данных для статистики")
        return
    photo_name = generate_stats_chart(rows, message.from_user.id)
    await message.answer_photo(photo=FSInputFile(photo_name))
    os.remove(photo_name)



@router.callback_query(F.data == "cancel")
async def delete_callback(callback: types.CallbackQuery, db):
    await callback.answer("Расход удален!")
    logger.info(f"Пользователь {callback.from_user.id} удалил свой последний расход")
    await db.delete_last_expense(callback.from_user.id)
    await callback.message.edit_text("Запись успешно удалена!")



@router.message(F.text.lower().in_({"cancel ❌", "cancel", "отмена"}))
async def delete_message_handler(message: types.Message, db):
    logger.info(f"Пользователь {message.from_user.id} удалил свой последний расход через меню")
    await db.delete_last_expense(message.from_user.id)
    await message.answer("Последняя запись успешно удалена!")



@router.message(F.text.lower().in_({"export 📁", "export", "экспорт"}))
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