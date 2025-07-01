from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.category import add_category, get_category_by_name, delete_category_by_id
from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.admin import admin_category_keyboard
from apps.keyboards.inline.category import admin_category_detail_keyboard, CategoryDetail
from apps.states.admin import CategoryAdd, AdminMainMenu
from loader import _

router = Router()


@router.message(IsAdmin(), F.text.in_(["Categories 🍴"]))
async def admin_category_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.set_state(AdminMainMenu.category)

    text = "Category menu"
    await message.answer(
        text=text,
        reply_markup=await admin_category_keyboard(
            session=session, chat_id=message.chat.id
        ))


@router.message(IsAdmin(), AdminMainMenu.category, F.text.in_(["Add category 🍴"]))
async def add_category_handler(message: types.Message, state: FSMContext):
    text = _("Enter name in uzbek")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryAdd.name_uz)


@router.message(IsAdmin(), CategoryAdd.name_uz)
async def add_category_handler(message: types.Message, state: FSMContext):
    await state.update_data(uz=message.text)
    text = _("Enter name in russian")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryAdd.name_ru)


@router.message(IsAdmin(), CategoryAdd.name_ru)
async def add_category_handler(message: types.Message, state: FSMContext):
    await state.update_data(ru=message.text)
    text = _("Enter name in english")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryAdd.name_en)


@router.message(IsAdmin(), CategoryAdd.name_en)
async def add_category_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(en=message.text)

    data = await state.get_data()
    if await add_category(session=session, data=data):
        text = _("Category is added")
    else:
        text = _("Something getting wrong, please try again later")
    await message.answer(
        text=text, reply_markup=await admin_category_keyboard(
            session=session, chat_id=message.chat.id
        ))
    await state.set_state(AdminMainMenu.category)


@router.callback_query(IsAdmin(), AdminMainMenu.category, CategoryDetail.filter(F.act == "delete_category"))
async def admin_category_detail_handler(
        call: CallbackQuery,
        callback_data: CategoryDetail,
        session: AsyncSession

):
    if await delete_category_by_id(
            session=session,
            category_id=callback_data.category_id
    ):
        await call.answer(text="Category is deleted ✅")
        await call.message.delete()
        text = "Category menu"
        await call.message.answer(
            text=text,
            reply_markup=await admin_category_keyboard(
                session=session, chat_id=call.message.chat.id
            ))
    else:
        await call.answer(text="Something went wrong ❌")


@router.message(IsAdmin(), AdminMainMenu.category)
async def accept_all_messages_category_handler(
        message: types.Message,
        session: AsyncSession
):
    category = await get_category_by_name(session=session, name=message.text)
    if category:
        text = f"""
Uzbek: {category.name['uz']}
Russian: {category.name['ru']}
English: {category.name['en']}
"""
        await message.answer(text=text,
                             reply_markup=await admin_category_detail_keyboard(
                                 category=category
                             ))
