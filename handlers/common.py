import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards import get_main_kb



router = Router()


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log", encoding="utf-8")
logger = logging.getLogger(__name__)


@router.message(F.text.lower() == "start")
@router.message(Command("start"))
async def start_handler(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} зарегистрировался.")
    await message.answer("Привет!", reply_markup=get_main_kb())



@router.message(F.text.lower() == "info")
@router.message(Command("info"))
async def info_handler(message: types.Message):
    await message.answer("Это финансовый бот на Python, он поможет тебе справится со всеми тратами")



@router.message(F.text.lower() == "back")
@router.message(Command("back"))
async def back_handler(message: types.Message):
    await start(message)