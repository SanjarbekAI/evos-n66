from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.admin import admin_main_menu
from apps.keyboards.default.user import user_main_menu_keyboard
from apps.states.admin import AdminMainMenu
from apps.states.user import Feedback
from loader import _

router = Router()


@router.message(IsAdmin(), F.text.in_(["Back ⬅️"]), AdminMainMenu.product)
@router.message(IsAdmin(), F.text.in_(["Back ⬅️"]), AdminMainMenu.category)
async def back_admin_main_menu(message: types.Message, state: FSMContext):
    text = _("Assalomu alaykum, admin 🫡")
    await message.answer(text=text, reply_markup=admin_main_menu)
    await state.clear()


@router.message(Feedback.feedback, F.text.in_(["Back ⬅️"]))
async def back_user_main_menu(message: types.Message, state: FSMContext):
    text = "Main menu"
    await message.answer(text=text, reply_markup=await user_main_menu_keyboard())
    await state.clear()
