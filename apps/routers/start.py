from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.user import get_user
from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.admin import admin_main_menu
from apps.keyboards.default.user import user_main_menu_keyboard
from apps.keyboards.inline.user import languages
from apps.states.user import Register
from loader import _

router = Router()


@router.message(Command('start'), IsAdmin())
async def admin_start_handler(message: types.Message):
    text = _("Assalomu alaykum, admin 🫡")
    await message.answer(text=text, reply_markup=admin_main_menu)


@router.message(Command('start'))
async def user_start_handler(message: types.Message, state: FSMContext, session: AsyncSession):
    user = await get_user(chat_id=message.chat.id, session=session)
    if not user:
        text = "Assalomu alaykum, please select the language !"
        await message.answer(text=text, reply_markup=languages)
        await state.set_state(Register.language)
    else:
        text = "Assalomu alaykum !"
        await message.answer(text=text, reply_markup=await user_main_menu_keyboard())
