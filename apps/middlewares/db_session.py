from typing import Awaitable, Callable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core.session import AsyncSessionLocal


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with AsyncSessionLocal() as session:
            data["session"] = session
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e
