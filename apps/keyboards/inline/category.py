from typing import Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.category import get_categories
from apps.db_queries.user import get_user
from core.models import Category
from loader import _


class CategoryDetail(CallbackData, prefix="category_detail"):
    act: str
    category_id: int


async def admin_category_inline_keyboard(session: AsyncSession, chat_id: int):
    user = await get_user(session=session, chat_id=chat_id)
    lang = user.language or "en"

    categories: Sequence[Category] = await get_categories(session=session)
    keyboard = []
    row = []
    for category in categories:
        name = category.name.get(lang, category.name.get("en", "Unnamed"))
        row.append(InlineKeyboardButton(text=name, callback_data=str(category.id)))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


async def admin_category_detail_keyboard(category):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=_("Delete ❌"),
                             callback_data=CategoryDetail(act="delete_category", category_id=category.id).pack()),
        InlineKeyboardButton(text=_("Update ✍️"),
                             callback_data=CategoryDetail(act="update_category", category_id=category.id).pack()),
    ]])
