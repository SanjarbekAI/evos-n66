from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.product import add_product
from apps.filters.is_admin import IsAdmin
from apps.keyboards.default.product import admin_product_keyboard
from apps.keyboards.inline.category import admin_category_inline_keyboard
from apps.states.admin import ProductAdd, AdminMainMenu
from loader import _

router = Router()


@router.message(IsAdmin(), F.text.in_(["Products 🍴"]))
async def admin_product_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.set_state(AdminMainMenu.product)
    text = _("Product menu")
    await message.answer(
        text=text,
        reply_markup=await admin_product_keyboard(
            session=session, chat_id=message.chat.id
        ))


@router.message(IsAdmin(), F.text.in_(["Add product 🍴"]))
async def add_product_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    text = _("Please, select the category")
    await message.answer(text=text, reply_markup=await admin_category_inline_keyboard(
        session=session, chat_id=message.chat.id
    ))
    await state.set_state(ProductAdd.category)


@router.callback_query(IsAdmin(), ProductAdd.category)
async def admin_category_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(category_id=int(call.data))
    text = _("Enter name in uzbek")
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.name_uz)


@router.message(IsAdmin(), ProductAdd.name_uz)
async def add_product_handler(message: types.Message, state: FSMContext):
    name = {'uz': message.text}
    await state.update_data(name=name)
    text = _("Enter name in russian")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.name_ru)


@router.message(IsAdmin(), ProductAdd.name_ru)
async def add_product_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name', {})
    name['ru'] = message.text
    await state.update_data(name=name)

    text = _("Enter name in english")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.name_en)


@router.message(IsAdmin(), ProductAdd.name_en)
async def add_product_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name', {})
    name['en'] = message.text
    await state.update_data(name=name)

    text = _("Enter about in uzbek")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.about_uz)


@router.message(IsAdmin(), ProductAdd.about_uz)
async def add_product_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    about = data.get('about', {})
    about['uz'] = message.text
    await state.update_data(about=about)

    text = _("Enter about in russian")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.about_ru)


@router.message(IsAdmin(), ProductAdd.about_ru)
async def add_product_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    about = data.get('about', {})
    about['ru'] = message.text
    await state.update_data(about=about)

    text = _("Enter about in english")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.about_en)


@router.message(IsAdmin(), ProductAdd.about_en)
async def add_product_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    about = data.get('about', {})
    about['en'] = message.text
    await state.update_data(about=about)

    text = _("Enter product price")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.price)


@router.message(IsAdmin(), ProductAdd.price)
async def add_product_handler(message: types.Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    text = _("Enter product image")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProductAdd.image)


@router.message(IsAdmin(), ProductAdd.image, F.photo)
async def add_product_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    if await add_product(session=session, data=data):
        text = _("Successfully added ✅")
    else:
        text = _("Something went wrong, please try again later")
    await message.answer(text=text, reply_markup=await admin_product_keyboard(
        session=session, chat_id=message.chat.id
    ))
    await state.clear()
