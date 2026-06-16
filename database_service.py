
class DatabaseLayer():
    def __init__(self, pool):
        self.pool = pool
    async def add_user(self, telegram_id, username, first_name):
        await self.pool.execute(
        "INSERT INTO users (telegram_id, username, first_name) VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING",
        telegram_id, username, first_name
    )

    async def db_check_user(self, telegram_id):
        result_id = await self.pool.fetchval("SELECT 1 FROM users WHERE telegram_id = $1", telegram_id)
        return result_id is not None
