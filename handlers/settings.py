import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards import get_settings_kb, get_main_kb
from database import get_user_name, update_user_name
from states import Profile
from aiogram.fsm.context import FSMContext

router = Router()


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log", encoding="utf-8")
logger = logging.getLogger(__name__)


@router.message(F.text.lower() == "settings")
@router.message(Command("settings"))
async def settings(message: types.Message):
    current_name = get_user_name(message.from_user.id)
    await message.answer(f"Твое имя: {current_name}, Что изменим? ", reply_markup=get_settings_kb())


@router.message(F.text.lower() == "изменить имя")
@router.message(Command("изменить имя"))
async def change_name(message: types.Message, state: FSMContext):
    await state.set_state(Profile.name)
    await message.answer("Как тебя зовут?")


@router.message(Profile.name)
async def name(message: types.Message, state: FSMContext):
    update_user_name(message.from_user.id, message.text)
    await state.clear()
    await message.answer(f"Имя {message.text} сохранено!")