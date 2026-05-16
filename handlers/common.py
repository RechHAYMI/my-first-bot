import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards import get_main_kb
from aiogram.fsm.context import FSMContext
from states import Profile
from database import db_add_user, check_user



router = Router()


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log", encoding="utf-8")
logger = logging.getLogger(__name__)


@router.message(F.text.lower() == "stop")
@router.message(Command("stop"))
async def stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено", reply_markup=get_main_kb())



@router.message(F.text.lower() == "start")
@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    if check_user(message.from_user.id):
        await message.answer("Рад возвращению!", reply_markup=get_main_kb())
    else:
        await state.set_state(Profile.name)
        logger.info(f"Пользователь {message.from_user.id} зарегистрировался.")
        await message.answer("Привет!Как тебя зовут?")


@router.message(Profile.name)
async def process_name(message: types.Message, state: FSMContext):
    db_add_user(message.from_user.id, message.text, message.from_user.username)       
    await state.clear()
    await message.answer("Имя сохранено", reply_markup=get_main_kb())


@router.message(F.text.lower() == "info")
@router.message(Command("info"))
async def info_handler(message: types.Message):
    await message.answer("Это финансовый бот на Python, он поможет тебе справится со всеми тратами")



@router.message(F.text.lower() == "back")
@router.message(Command("back"))
async def back_handler(message: types.Message, state: FSMContext):
    await start_handler(message, state)