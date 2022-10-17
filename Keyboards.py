from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/Добавить'))

    return kb
