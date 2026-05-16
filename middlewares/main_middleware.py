from database import db_add_user, user_exists
from aiogram import BaseMiddleware
from typing import Dict, Any, Callable
from config import ADMIN_ID

class ShadowMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = event.from_user
        if user is not None and not user_exists(user.id):
            db_add_user(user.id, user.first_name, user.username)
        data["is_admin"] = (user.id == ADMIN_ID)
        return await handler(event, data)