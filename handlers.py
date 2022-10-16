from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from Keyboards import get_kb
from main import dp
from sql import db_start

storage = MemoryStorage()

HELP_COMMAND = """
<b>/start</b> - <em>начало работы с ботом</em>
<b>/description</b> - <em>описание бота</em>
<b>/help</b> - <em>список команд</em>
<b>/add</b> - <em>добавить материал</em>
<b>/search</b> - <em>поиск материала по базе</em>
"""


class ItemState(StatesGroup):
    item = State()
    item_size = State()


async def on_startup(_):
    await db_start()
    print('Бот успешно запущен!')
    print('База данных запущена!')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        f'Привет, <b>{message.from_user.first_name}</b>! Добро пожаловать в бот по поиску остатков\nДля помощи нажми > /help',
        reply_markup=get_kb(), parse_mode='HTML')
    # await db_start()
    # await create_profile(user_id=message.from_user.id)
    # await message.delete()


@dp.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await message.answer('описание бота')
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(HELP_COMMAND,
                        parse_mode='HTML')


# @dp.message_handler(commands=('add'))
# async def add_command(message: types.Message):
#     # user_text = message.text
#     await bot.send_message(message.chat.id, 'Введи буквенно-цифровой артикул латинскими буквами')
#     await add_det(detail_size=message.text, user_id=message.from_user.id, username=message.from_user.username)
#     # await bot.send_message("Введи буквенно-цифровой артикул латинскими буквами")
#     # await bot.send_message(message.chat.id, message.text)
#
#     await bot.send_message(message.from_user.id, text='Запись добавлена в базу данных!')
#     # await message.delete()


@dp.message_handler(commands=['add'])
async def add_command(message: types.Message):
    await message.answer('Введи буквенно-цифровой артикул латинскими буквами или название материала')
    await ItemState.item.set()
    # await add_det(item=message.text, user_id=message.from_user.id, username=message.from_user.username)
    # await bot.send_message("Введи буквенно-цифровой артикул латинскими буквами")
    # await bot.send_message(message.chat.id, message.text)

    # await bot.send_message(message.from_user.id, text='Запись добавлена в базу данных!')


@dp.message_handler(state=ItemState.item)
async def load_item(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['item'] = message.text
    await state.update_data(item=message.text)
    await message.answer('Теперь введи размеры детали!')
    await ItemState.next()


dp.message_handler(state=ItemState.item_size)
async def load_item_size(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['item_size'] = message.text
    await state.update_data(item_size=message.text)
    await message.answer('Запись успешно добавлена в базу!')
    data = await state.get_data()
    await message.answer(f"материал: {data['item']}\n"
                         f"размер: {data['item_size']}")
    await state.finish()

# @dp.message_handler(commands=['search'])
# async def search_command(message: types.Message) -> None:
#     await message.answer('Введи буквенно-цифровой артикул латинскими буквами')
#     await message.delete()
