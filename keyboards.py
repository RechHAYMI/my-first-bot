from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



def get_main_kb():
    buttons = [
        [KeyboardButton(text="Start"), KeyboardButton(text="Info")],
        [KeyboardButton(text="Settings"), KeyboardButton(text="Stats")],
        [KeyboardButton(text="Canсel"), KeyboardButton(text="Export")],
        [KeyboardButton(text="Добавить расход")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)



def get_delete_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить ❌", callback_data="delete_exp")]
    ])


def get_settings_kb():
    buttons = [
        [KeyboardButton(text="Изменить имя"), KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)



def get_categor_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Еда", callback_data="cat_food")],
        [InlineKeyboardButton(text="Такси", callback_data="cat_taxi")]
    ])