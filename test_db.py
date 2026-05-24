import asyncio
import asyncpg

async def setup_database():
    print("Подключение к PostgreSQL для создания таблицы...")
    try:
        conn = await asyncpg.connect(
            user='alex_developer',
            password='my_secret_password',
            database='bot_data',
            host='127.0.0.1',
            port=5432
        )
        
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            username VARCHAR(50),
            first_name VARCHAR(100),
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        
        await conn.execute(create_table_query)
        print("Таблица 'users' успешно создана (или уже существовала)!")

        
        await conn.close()
        print("Соединение закрыто.")

    except Exception as e:
        print(f"Ошибка: {e}")

asyncio.run(setup_database())