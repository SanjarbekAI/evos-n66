from aiogram import types
from aiogram.filters import BaseFilter

from core.config import ADMINS


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message):
        return message.from_user.id in ADMINS
