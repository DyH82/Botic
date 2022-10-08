from aiogram import Bot, Dispatcher, executor

from config import BOT_TOKEN


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    from handlers import dp, on_startup

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
