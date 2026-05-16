import asyncio
import os
import logging
from handlers import common, expenses, settings 
from database import init_db
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Broadcast
from middlewares.main_middleware import ShadowMiddleware
from database import init_db, all_user_id



load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log", encoding="utf-8")
logger = logging.getLogger(__name__)



bot = Bot(token=TOKEN)

dp = Dispatcher()


dp.message.outer_middleware(ShadowMiddleware())
dp.callback_query.outer_middleware(ShadowMiddleware())



@dp.message(Command("sendall"))
async def mailing_mode(message: types.Message, state: FSMContext, is_admin: bool):
    if is_admin:
        state.set_state(Broadcast.text)
        await message.answer(f"{message.from_user.id} Жду контент для рассылки")
    else:
        await message.answer("Отказано в доступе")



@dp.message(Broadcast.text)
async def mailing_logic(message: types.Message, state: FSMContext):
    users = all_user_id()
    count = 0
    errors = 0
    for user in users:
        try:
            await message.copy_to(chat_id=user[0])
            count += 1
        except Exception as e:
            print(f"Не удалось отправить {user[0]}. Ошибка: {e}")
            errors += 0
    await message.answer(f"Рассылка завершена! Получили: {count}, Не смогли получить: {errors}")
    await state.clear()



async def main():
    init_db()
    logger.info("Бот запущен и готов к работе")
    dp.include_router(common.router)
    dp.include_router(expenses.router)
    dp.include_router(settings.router)
    await dp.start_polling(bot)


asyncio.run(main())