from aiogram.utils.i18n import I18nMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.user import get_user


async def get_lang(user_id, session: AsyncSession):
    user = await get_user(user_id, session)
    return user.language if user else "en"


class LanguageMiddleware(I18nMiddleware):
    async def get_locale(self, event, data) -> str:
        user = getattr(event, "from_user", data.get("event_from_user"))
        session: AsyncSession = data.get("session")

        if not user or not session:
            return "en"
        return await get_lang(user.id, session)
