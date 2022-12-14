from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN

# proxy_url = 'http://proxy.server:3128'
# bot = Bot(BOT_TOKEN, proxy=proxy_url)

bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

if __name__ == '__main__':
    from handlers import dp, on_startup

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
