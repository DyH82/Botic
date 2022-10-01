from aiogram import types
from aiogram.types import Message

from main import bot, dp

HELP_COMMAND = """
/help - список команд
/start - начало работы с ботом
"""


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)


@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await message.answer(text='Добро пожаловать в бот по поиску остатков\n Для помощи введи команду /help')
    await message.delete()