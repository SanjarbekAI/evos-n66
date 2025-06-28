import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category


async def add_category(session: AsyncSession, data: dict):
    try:
        category = Category(
            name=data
        )
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category.id
    except Exception as e:
        logging.error(e)
        await session.rollback()
        return None


async def get_categories(session: AsyncSession):
    try:
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        return categories
    except Exception as e:
        logging.error(e)
        return None
