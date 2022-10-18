from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from Keyboards import get_kb
from main import dp
from sql import db_start, add_item, add_profile

storage = MemoryStorage()

HELP_COMMAND = """
<b>/start</b> - <em>начало работы с ботом</em>
<b>/description</b> - <em>описание бота</em>
<b>/help</b> - <em>список команд</em>
<b>/add</b> - <em>добавить материал</em>
<b>/search</b> - <em>поиск материала по базе</em>
"""


class ItemState(StatesGroup):

    item_brand = State()
    item = State()
    item_name = State()
    item_length = State()
    item_width = State()


async def on_startup(_):
    await db_start()
    print('Бот успешно запущен!')
    # print('База данных запущена!')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        f'Привет, <b>{message.from_user.first_name}</b>! Добро пожаловать в бот по поиску остатков\nДля помощи нажми > /help',
        reply_markup=get_kb(), parse_mode='HTML')
    await add_profile(user_id=message.from_user.id)


@dp.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await message.answer('описание бота')
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(HELP_COMMAND,
                        parse_mode='HTML')


@dp.message_handler(commands=['add'])
async def add_command(message: types.Message):
    await message.reply('Введи производителя(Бренд). Например Egger:')
    await ItemState.item_brand.set()


@dp.message_handler(state=ItemState.item_brand)
async def load_item_brand(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['item_brand'] = message.text
    await state.update_data(item_brand=message.text)
    await message.reply('Введи буквенно-цифровой артикул латинскими буквами:')
    await ItemState.next()


@dp.message_handler(state=ItemState.item)
async def load_item(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['item'] = message.text
    await state.update_data(item=message.text)
    await message.reply('Введи название материала:')
    await ItemState.next()


@dp.message_handler(state=ItemState.item_name)
async def load_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['item_name'] = message.text
    await state.update_data(item_name=message.text)
    await message.reply('Введи длину детали в "мм":')
    await ItemState.next()


@dp.message_handler(state=ItemState.item_length)
async def load_item_length(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['item_length'] = message.text
    await state.update_data(item_length=message.text)
    await message.reply('Введи ширину детали в "мм":')
    await ItemState.next()


@dp.message_handler(state=ItemState.item_width)
async def load_item_width(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['item_width'] = message.text
    await state.update_data(item_width=message.text)
    await add_item(state, user_id=message.from_user.id)
    await message.reply('Запись успешно добавлена в базу!')
    await message.answer(f"производитель: {data['item_brand']}\n"
                         f"артикул: {data['item']}\n"
                         f"название: {data['item_name']}\n"
                         f"размер детали: {data['item_length'] + '*' + data['item_width']}")
    await state.finish()

# @dp.message_handler(commands=['search'])
# async def search_command(message: types.Message) -> None:
#     await message.answer('Введи буквенно-цифровой артикул латинскими буквами')
#     await message.delete()
