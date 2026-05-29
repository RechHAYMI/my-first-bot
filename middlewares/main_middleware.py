from database import db_add_user
from aiogram import BaseMiddleware
from typing import Dict, Any, Callable
from config import ADMIN_ID

class ShadowMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = event.from_user
        if user is not None:
            pool = data.get("pool")
            await db_add_user(pool, user.id, user.username, user.first_name)
        data["is_admin"] = (user.id == ADMIN_ID)
        return await handler(event, data)