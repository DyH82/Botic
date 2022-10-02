from aiogram import types

from main import dp
from sql import db_start, create_profile

HELP_COMMAND = """
<b>/start</b> - <em>начало работы с ботом</em>
<b>/description</b> - <em>описание бота</em>
<b>/help</b> - <em>список команд</em>
<b>/add</b> - <em>добавить материал</em>
<b>/search</b> - <em>поиск материала по базе</em>
"""


async def on_startup(_):
    # await db_start()
    print('Бот успешно запущен!')

    print('База данных запущена!')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        f'{message.from_user.first_name}, добро пожаловать в бот по поиску остатков\nДля помощи нажми > /help')
    await db_start()

    await create_profile(user_id=message.from_user.id)
    # await message.delete()

@dp.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await message.answer(text='описание бота')
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND,
                        parse_mode='HTML')


@dp.message_handler(commands=['add'])
async def add_command(message: types.Message):
    await message.answer(text='Введи буквенно-цифровой артикул латинскими буквами')
    await message.delete()



@dp.message_handler(commands=['search'])
async def search_command(message: types.Message):
    await message.answer(text='Введи буквенно-цифровой артикул латинскими буквами')
    await message.delete()
