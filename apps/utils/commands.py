from aiogram import Bot
from aiogram.types import BotCommand


async def set_my_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start to work 🚀"),
        BotCommand(command="help", description="Get information 📝")
    ]
    await bot.set_my_commands(commands=commands)
