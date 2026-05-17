import asyncio
from database import all_user_id
from main import bot


async def shadow_parser():
    last_status = "ok"
    while True:
        new_status = "ok"
        print("Проверяю сайт...")
        users = all_user_id()
        if new_status != last_status:
            for user in users:
                try:
                    await bot.send_message(chat_id=user[0], text="Вышло обновление!")
                    await asyncio.sleep(0.05)
                except Exception as e:
                    print(f"Не удалось отправить {user[0]}. Ошибка: {e}")
            last_status = new_status
    
        await asyncio.sleep(10)