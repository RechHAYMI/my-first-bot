from aiogram.fsm.state import StatesGroup, State

class Profile(StatesGroup):
    name = State()


class FSMExpense(StatesGroup):
    categor = State()
    sum = State()