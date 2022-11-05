from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

positions_cb = CallbackData('position', 'id', 'action')


#  ин-лайн клавиатура
def get_positions_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Просмотр всех позиций', callback_data='get_all_positions')],
        [InlineKeyboardButton('Поиск материала', callback_data='get_position_')],
        [InlineKeyboardButton('Добавить материал', callback_data='add_new_position')]
    ])

    return ikb


# ################# для админа

def get_edit_position(id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Редактировать материал', callback_data=positions_cb.new(id, 'edit'))],
        [InlineKeyboardButton('Удалить материал', callback_data=positions_cb.new(id, 'delete'))]
    ])

    return ikb
####################

# обычная кнопка
def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('/Меню')]
    ], resize_keyboard=True)

    return kb


# отмена
def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('/cancel')]
    ], resize_keyboard=True)

    return kb
