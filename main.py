from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN

storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

if __name__ == '__main__':
    from handlers import dp, on_startup

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
