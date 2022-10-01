from aiogram import Bot, Dispatcher, executor, types

from config import BOT_TOKEN


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)