from typing import Sequence

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.category import get_categories
from apps.db_queries.user import get_user
from core.models import Category
from loader import _

admin_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Products 🍴"),
            KeyboardButton(text="Categories 🍴"),
        ],
        [
            KeyboardButton(text="Users 👯"),
            KeyboardButton(text="Orders 📝")
        ],
        [
            KeyboardButton(text="Statistics 📊"),
            KeyboardButton(text="Settings ⚙️"),
        ]
    ], resize_keyboard=True
)


async def admin_category_keyboard(session: AsyncSession, chat_id: int):
    user = await get_user(session=session, chat_id=chat_id)
    lang = user.language or "en"

    categories: Sequence[Category] = await get_categories(session=session)
    keyboard = [
        [
            KeyboardButton(text=_("Add category 🍴")),
            KeyboardButton(text=_("Back ⬅️"))
        ]
    ]
    row = []
    for category in categories:
        name = category.name.get(lang, category.name.get("en", "Unnamed"))
        row.append(KeyboardButton(text=name))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
