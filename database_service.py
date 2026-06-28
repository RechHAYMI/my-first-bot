##если кто то читает,ниже описание для самого меня
class DatabaseLayer(): #создаем класс что создать коробку
    def __init__(self, pool): #инит конструктор
        self.pool = pool # указываем что пул это селф пул тем самым помещаем его в коробку
    async def add_user(self, telegram_id, username, first_name): # копируем функциюю из датабейз но только засовываем пул в коробку
        await self.pool.execute( # sql запрос
        "INSERT INTO users (telegram_id, username, first_name) VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING",
        telegram_id, username, first_name
        )
    async def db_check_user(self, telegram_id): # тоже копируем функцию и ниже запросы, но только пул в коробке
        result_id = await self.pool.fetchval("SELECT 1 FROM users WHERE telegram_id = $1", telegram_id)
        return result_id is not None
