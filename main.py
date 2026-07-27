import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from database import init_postgres
from dotenv import load_dotenv
from parser import shadow_parser
from handlers import common, expenses, settings, admin
from middlewares.main_middleware import ShadowMiddleware
from middlewares.ThrottlingMiddleware import ThrottlingMiddleware
from config import bot, ADMIN_ID


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s", 
    filename="bot.log", 
    encoding="utf-8"
)
logger = logging.getLogger(__name__)



dp = Dispatcher()

dp.message.middleware(ThrottlingMiddleware(limit=1.0))
dp.message.middleware(ShadowMiddleware())

dp.callback_query.middleware(ThrottlingMiddleware(limit=1.0))
dp.callback_query.middleware(ShadowMiddleware())

async def main():
    pool = await init_postgres()
    dp.include_routers(common.router, expenses.router, settings.router, admin.router)
    asyncio.create_task(shadow_parser(pool))
    await dp.start_polling(bot, pool=pool)
    logger.info("Бот запущен и готов к работе")

if __name__ == "__main__":
    asyncio.run(main())
