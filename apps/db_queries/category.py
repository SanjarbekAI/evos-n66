import logging

from sqlalchemy import select, or_, delete
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


async def get_category_by_name(session: AsyncSession, name: str):
    try:
        result = select(Category).where(
            or_(
                Category.name["uz"].astext == name,
                Category.name["ru"].astext == name,
                Category.name["en"].astext == name,
            )
        )
        result = await session.execute(result)
        category = result.scalars().one_or_none()
        return category
    except Exception as e:
        logging.error(e)
        return None


async def delete_category_by_id(session: AsyncSession, category_id: int):
    try:
        category = delete(Category).where(Category.id == category_id)
        await session.execute(category)
        await session.commit()
        return True
    except Exception as e:
        logging.error(e)
        return None
