import asyncpg

async def init_postgres():
    pool = await asyncpg.create_pool(
        user='alex_developer',
        password='my_secret_password',
        database='bot_data',
        host='127.0.0.1',
        port=5432
    )

    await pool.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            username VARCHAR(50),
            first_name VARCHAR(100),
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
    await pool.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT REFERENCES users(telegram_id),
            amount NUMERIC(10, 2) NOT NULL,
            category VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)


    await pool.execute("""
        CREATE TABLE IF NOT EXISTS custom_categories (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT REFERENCES users(telegram_id),
        category_name VARCHAR(50),
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    return pool