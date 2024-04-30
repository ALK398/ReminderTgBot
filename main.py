import asyncio

from aiogram import Bot, Dispatcher

from data_storage.session_info import reset_info

from logging_data.logging_bot import start_logging
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers


async def main():
    reset_info()
    start_logging()

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    dp = Dispatcher()

    dp.include_router(user_handlers.router_logging)
    dp.include_router(user_handlers.router_note)
    dp.include_router(user_handlers.router_reminder)

    dp.include_router(other_handlers.router)

    await dp.start_polling(bot)

    await user_handlers.check_reminder(bot)


if __name__ == '__main__':
    asyncio.run(main())
