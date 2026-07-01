import logging



from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import get_settings_kb, get_main_kb
from states import SettingsStates


router = Router()


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log", encoding="utf-8")
logger = logging.getLogger(__name__)


@router.message(F.text.lower() == "settings")
@router.message(Command("settings"))
async def settings(message: types.Message, db):
    current_name = await db.get_user_name(message.from_user.id)
    await message.answer(f"Твое имя: {current_name}, Что изменим? ", reply_markup=get_settings_kb())


@router.message(F.text.lower() == "изменить имя")
async def change_name(message: types.Message, state: FSMContext, db):
    await state.set_state(SettingsStates.waiting_for_name)
    await message.answer("Как тебя зовут?")


@router.message(SettingsStates.waiting_for_name)
async def name(message: types.Message, state: FSMContext, db):
    if len(message.text) > 1 and len(message.text) < 15 and message.text.isalpha():
        await db.update_user_name(message.text, message.from_user.id)
        await state.clear()
        await message.answer(f"Имя {message.text} сохранено!", reply_markup=get_main_kb())
    else:
        await message.answer("Ошибка! Имя должно состоять только из букв и быть от 2 до 15 символов")
        return