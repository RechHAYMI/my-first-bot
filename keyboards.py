from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class CategoryCallback(CallbackData, prefix="expense"):
    name: str

class DeleteCategoryCallback(CallbackData, prefix="del_cat"):
    id: int

def get_main_kb():
    buttons = [
        [KeyboardButton(text="Start 🚀"), KeyboardButton(text="Info ℹ️")],
        [KeyboardButton(text="Settings ⚙️"), KeyboardButton(text="Stats 📊")],
        [KeyboardButton(text="Cancel ❌"), KeyboardButton(text="Export 📁")],
        [KeyboardButton(text="Add expenses 💸")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_delete_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить ❌", callback_data="cancel")]
    ])

def get_settings_kb():
    buttons = [
        [KeyboardButton(text="Изменить имя")],
        [KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_categor_kb(user_categories):
    builder = InlineKeyboardBuilder()
    builder.button(text="Еда 🍔", callback_data=CategoryCallback(name="food").pack())
    builder.button(text="Такси 🚕", callback_data=CategoryCallback(name="taxi").pack())
    for category in user_categories:
        builder.button(text=category['category_name'], callback_data=CategoryCallback(name=category['category_name']).pack()) 
    builder.button(text="+ new categories", callback_data=CategoryCallback(name="+ new categories").pack())
    builder.button(text="Удалить категорию 🗑", callback_data="open_delete_menu") 
    builder.adjust(2)
    return builder.as_markup()

def get_delete_category_kb(user_categories):
    builder = InlineKeyboardBuilder()
    for category in user_categories:
        builder.button(text=category['category_name'] + " ❌", callback_data=DeleteCategoryCallback(id=category['id']).pack())
    builder.button(text="Отмена", callback_data="cancel_deletion")
    builder.adjust(1)
    return builder.as_markup()