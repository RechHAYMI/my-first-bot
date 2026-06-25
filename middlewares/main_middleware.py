#если также ктото читает, это заметка для меня, я писал все сам, но забыл, поэтому обьясню
from database import db_add_user #ниже иморты всякие
from aiogram import BaseMiddleware
from typing import Dict, Any, Callable
from config import ADMIN_ID

class ShadowMiddleware(BaseMiddleware): #создаю класс на базе BaseMiddleware
    async def __call__(self, handler, event, data): # это дверь, через которую проходит абсолютно любое действие пользователя
        pool = data.get("pool") # обозначаю что такое пул
        user = event.from_user # Обозначаю что такое user
        if user is not None and pool: # проверяю есть ли юзер и было ли взаимодействие с пулом
            await db_add_user(pool, user.id, user.username, user.first_name) # если он не зареган то добавляю в дб
        data["is_admin"] = (user.id == ADMIN_ID) # если его телеграм айди равен админ айди то выдаю админку
        data["db"] = DatabaseLayer(pool) # обозначаю что db это DatabaseLayer то есть коробка с пулом
        return await handler(event, data) #Middleware говорит боту: «Я всё проверил, коробку в сумку положил, теперь пропускай событие дальше к хэндлеру, вот тебе обновленная сумка data».