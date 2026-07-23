from aiogram.fsm.state import StatesGroup, State

class Profile(StatesGroup):
    name = State()


class FSMExpense(StatesGroup):
    categor = State()
    sum = State()
    waiting_for_custom_categories = State()


class Broadcast(StatesGroup):
    text = State()

class SettingsStates(StatesGroup):
    waiting_for_name = State()