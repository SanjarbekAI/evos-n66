import logging
from asyncio import run

from aiogram import Bot

from apps.middlewares.db_session import DbSessionMiddleware
from apps.middlewares.language import LanguageMiddleware
from apps.middlewares.subscription import SubscribeMiddleware
from apps.routers import start, register, feedback, backs, user_menu
from apps.utils.commands import set_my_commands
from core.config import DEVELOPER
from loader import dp, bot, i18n


async def startup(bot: Bot):
    await set_my_commands(bot)
    await bot.send_message(text="Bot start to work", chat_id=DEVELOPER)


async def shutdown(bot: Bot):
    await bot.send_message(text="Bot stopped", chat_id=DEVELOPER)


async def main():
    dp.include_router(router=start.router)
    dp.include_router(router=register.router)
    dp.include_router(router=feedback.router)
    dp.include_router(router=backs.router)
    dp.include_router(router=user_menu.router)

    dp.message.middleware.register(DbSessionMiddleware())
    dp.message.middleware.register(LanguageMiddleware(i18n=i18n))
    dp.message.middleware.register(SubscribeMiddleware())

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot, polling_timeout=0)


if __name__ == '__main__':
    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.ERROR
    )
    logging.getLogger("aiogram.event").setLevel(logging.ERROR)
    run(main())
