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
    return pool


async def db_add_user(pool, telegram_id, username, first_name):
    await pool.execute(
        "INSERT INTO users (telegram_id, username, first_name) VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING",
        telegram_id, username, first_name
    )


async def check_user(pool, telegram_id):
    result_id = await pool.fetchval("SELECT 1 FROM users WHERE telegram_id = $1", telegram_id)
    return result_id is not None


async def db_add_expense(pool, telegram_id, amount, category):
    await pool.execute(
        "INSERT INTO expenses (telegram_id, amount, category) VALUES ($1, $2, $3)",
        telegram_id, amount, category
    )


async def get_category_stats(pool, telegram_id):
    rows = await pool.fetch(
        "SELECT category, SUM(amount) FROM expenses WHERE telegram_id = $1 GROUP BY category",
        telegram_id,
    )
    return rows


async def delete_last_expense(pool, telegram_id):
    await pool.execute(
        "DELETE from expenses WHERE id = (SELECT id FROM expenses WHERE telegram_id = $1 ORDER BY created_at DESC LIMIT 1)",
        telegram_id,
    )


async def get_user_name(pool, telegram_id):
    row = await pool.fetchval(
        "SELECT first_name FROM users WHERE telegram_id = $1",
        telegram_id,
    )
    return row


async def update_user_name(pool, new_name, telegram_id):
    await pool.execute(
        "UPDATE users SET first_name = $1 WHERE telegram_id = $2",
        new_name, telegram_id
    )


async def all_user_id(pool):
    rows = await pool.fetch(
        "SELECT telegram_id FROM users"
    )
    return [row['telegram_id'] for row in rows]