import asyncio
from aiogram import Bot, Dispatcher
from config.settings import settings
from bot.handlers import base, auth, homework, errors


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(base.router)
    dp.include_router(auth.router)
    dp.include_router(homework.router)
    dp.include_router(errors.router)

    from services.database import init_db
    await init_db()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
