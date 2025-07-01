import asyncio
import logging

from aiogram import Bot

from apps.middlewares.db_session import DbSessionMiddleware
from apps.middlewares.language import LanguageMiddleware
from apps.middlewares.subscription import SubscribeMiddleware
from apps.routers import start, register, feedback, backs, user_menu
from apps.routers.admin import category, product
from apps.utils.commands import set_my_commands
from core.config import DEVELOPER
from loader import bot, dp, i18n

# bind localhost only to prevent any external access
WEB_SERVER_HOST = "127.0.0.1"
# Port for incoming request from reverse proxy. Should be any available port
WEB_SERVER_PORT = 8080

# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = "/webhook"
# Secret key to validate requests from Telegram (optional)
WEBHOOK_SECRET = "SECRET"


async def startup(bot: Bot):
    await set_my_commands(bot)
    # await bot.set_webhook(
    #     url=f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
    #     secret_token=WEBHOOK_SECRET,
    #     drop_pending_updates=True
    # )
    await bot.send_message(text="Bot start to work", chat_id=DEVELOPER)


async def shutdown(bot: Bot):
    await bot.send_message(text="Bot stopped", chat_id=DEVELOPER)


async def main():
    # admin routers
    dp.include_router(router=backs.router)
    dp.include_router(router=category.router)
    dp.include_router(router=product.router)

    # user routers
    dp.include_router(router=start.router)
    dp.include_router(router=register.router)
    dp.include_router(router=feedback.router)
    dp.include_router(router=user_menu.router)

    dp.message.middleware.register(DbSessionMiddleware())
    dp.callback_query.middleware.register(DbSessionMiddleware())
    dp.message.middleware.register(LanguageMiddleware(i18n=i18n))
    dp.message.middleware.register(SubscribeMiddleware())

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    # app = web.Application()
    #
    # webhook_requests_handler = SimpleRequestHandler(
    #     dispatcher=dp,
    #     bot=bot,
    #     secret_token=WEBHOOK_SECRET,
    # )
    # webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    #
    # setup_application(app, dp, bot=bot)
    #
    # web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    await dp.start_polling(bot, polling_timeout=0)


if __name__ == '__main__':
    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.ERROR
    )
    logging.getLogger("aiogram.event").setLevel(logging.ERROR)
    asyncio.run(main())
