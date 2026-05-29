import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from parser import shadow_parser
from handlers import common, expenses, settings
from database import init_postgres, all_user_id
from states import Broadcast
from middlewares.main_middleware import ShadowMiddleware
from config import bot, ADMIN_ID


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s", 
    filename="bot.log", 
    encoding="utf-8"
)
logger = logging.getLogger(__name__)



dp = Dispatcher()


dp.update.outer_middleware(ShadowMiddleware())

@dp.message(Command("sendall"))
async def mailing_mode(message: types.Message, state: FSMContext, is_admin: bool):
    if is_admin:
        state.set_state(Broadcast.text)
        await message.answer(f"{message.from_user.id} Жду контент для рассылки")
    else:
        await message.answer("Отказано в доступе")

@dp.message(Broadcast.text)
async def mailing_logic(message: types.Message, state: FSMContext):
    users = await all_user_id()
    count = 0
    errors = 0
    for user in users:
        try:
            await message.copy_to(chat_id=user[0])
            count += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            print(f"Не удалось отправить {user[0]}. Ошибка: {e}")
            errors += 1  
            
    await message.answer(f"Рассылка завершена! Получили: {count}, Не смогли получить: {errors}")
    await state.clear()

async def main():
    pool = await init_postgres()
    dp.include_routers(common.router, expenses.router, settings.router)
    asyncio.create_task(shadow_parser())
    await dp.start_polling(bot, pool=pool)
    logger.info("Бот запущен и готов к работе")

if __name__ == "__main__":
    asyncio.run(main())
