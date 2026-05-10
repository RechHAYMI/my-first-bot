from database import add_user, user_exists
from aiogram import BaseMiddleware


class DbCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = event.from_user
        if user is not None and not user_exists(user.id):
            add_user(user.id, user.first_name, user.username)
        return await handler(event, data)