from typing import Sequence

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.product import get_products
from apps.db_queries.user import get_user
from core.models import Product
from loader import _


async def admin_product_keyboard(session: AsyncSession, chat_id: int):
    user = await get_user(session=session, chat_id=chat_id)
    lang = user.language or "en"

    products: Sequence[Product] = await get_products(session=session)
    keyboard = [
        [
            KeyboardButton(text=_("Add product 🍴")),
            KeyboardButton(text=_("Back ⬅️"))
        ]
    ]
    row = []
    for product in products:
        name = product.name.get(lang, product.name.get("en", "Unnamed"))
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
