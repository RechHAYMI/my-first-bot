from aiogram import BaseMiddleware
from typing import Dict, Any, Callable
from config import ADMIN_ID



class DbCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):

        user_id = event.from_user.id

        data["is_admin"] = (user_id == ADMIN_ID)
        return await handler(event, data)