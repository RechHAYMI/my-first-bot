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
    return pool


async def db_add_user(pool, telegram_id, username, first_name):
    await pool.execute(
        "INSERT INTO users (telegram_id, username, first_name) VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING",
        telegram_id, username, first_name
    )


async def check_user(pool, telegram_id):
    result_id = await pool.fetchval("SELECT 1 FROM users WHERE telegram_id = $1", telegram_id)
    return result_id is not None