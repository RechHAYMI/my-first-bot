from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class CategoryCallback(CallbackData, prefix="expense"):
    name: str



def get_main_kb():
    buttons = [
        [KeyboardButton(text="Start"), KeyboardButton(text="Info")],
        [KeyboardButton(text="Settings"), KeyboardButton(text="Stats")],
        [KeyboardButton(text="Canсel"), KeyboardButton(text="Export")],
        [KeyboardButton(text="add expenses")]
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



def get_categor_kb(user_categories):
    builder = InlineKeyboardBuilder()
    builder.button(text="Еда", callback_data=CategoryCallback(name="food").pack())
    builder.button(text="Такси", callback_data=CategoryCallback(name="taxi").pack())
    for category in user_categories:
        builder.button(text=category['category_name'], callback_data=CategoryCallback(name=category['category_name']).pack())
    builder.button(text="+new categories", callback_data=CategoryCallback(name="+ new categories").pack())
    builder.adjust(2, 2)
    return builder.as_markup()