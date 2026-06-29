##если кто то читает,ниже описание для самого меня
class DatabaseLayer(): #создаем класс что создать коробку
    def __init__(self, pool): #инит конструктор
        self.pool = pool # указываем что пул это селф пул тем самым помещаем его в коробку
    async def add_user(self, telegram_id, username, first_name): # копируем функциюю из датабейз но только засовываем пул в коробку
        await self.pool.execute( # sql запрос
        "INSERT INTO users (telegram_id, username, first_name) VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING",
        telegram_id, username, first_name
        )


    async def check_user(self, telegram_id): # тоже копируем функцию и ниже запросы, но только пул в коробке
        result_id = await self.pool.fetchval("SELECT 1 FROM users WHERE telegram_id = $1", telegram_id)
        return result_id is not None


    async def add_expense(self, telegram_id, amount, category):
        await self.pool.execute(
            "INSERT INTO expenses (telegram_id, amount, category) VALUES ($1, $2, $3)",
            telegram_id, amount, category
        )


    async def get_category_stats(self, telegram_id):
        rows = await self.pool.fetch(
            "SELECT category, SUM(amount) FROM expenses WHERE telegram_id = $1 GROUP BY category",
            telegram_id,
        )
        return rows


    async def delete_last_expense(self, telegram_id):
        await self.pool.execute(
            "DELETE from expenses WHERE id = (SELECT id FROM expenses WHERE telegram_id = $1 ORDER BY created_at DESC LIMIT 1)",
            telegram_id,
        )


    async def get_user_name(self, telegram_id):
        row = await self.pool.fetchval(
            "SELECT first_name FROM users WHERE telegram_id = $1",
            telegram_id,
        )
        return row

    async def update_user_name(self, new_name, telegram_id):
        await self.pool.execute(
            "UPDATE users SET first_name = $1 WHERE telegram_id = $2",
            new_name, telegram_id
        )


    async def all_user_id(self):
        rows = await self.pool.fetch(
            "SELECT telegram_id FROM users"
        )
        return [row['telegram_id'] for row in rows]


    async def get_all_expenses(self, telegram_id):
        rows = await self.pool.fetch(
            "SELECT category, amount, created_at FROM expenses WHERE telegram_id = $1 ORDER BY created_at DESC",
            telegram_id
        )
        return rows