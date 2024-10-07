import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import Tortoise

from app.user import user
from config import TOKEN, DB_URL
from app.schedule import check_reminders


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_router(user)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await Tortoise.init(db_url=DB_URL, modules={"models": ["app.database.models"]})
    await Tortoise.generate_schemas()

    asyncio.create_task(check_reminders())
    # logging.debug('включенно')


async def shutdown(dispatcher: Dispatcher):
    # logging.debug('выключение')
    await Tortoise.close_connections()
    exit(0)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
