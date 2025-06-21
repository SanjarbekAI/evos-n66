from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from apps.db_queries.user import register
from apps.keyboards.default.user import phone_number_share, location_share, user_main_menu
from apps.states.user import Register

router = Router()


@router.callback_query(Register.language)
async def get_user_language_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(language=call.data, chat_id=call.message.chat.id)

    await call.message.answer(text="Please enter your full name")
    await state.set_state(Register.full_name)


@router.message(Register.full_name)
async def get_user_full_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    await message.answer(text="Please share your phone number", reply_markup=phone_number_share)
    await state.set_state(Register.phone_number)


@router.message(Register.phone_number, F.contact)
async def get_user_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data(
        phone_number=message.contact.phone_number,
        username=message.from_user.username
    )

    await message.answer(text="Please share your location", reply_markup=location_share)
    await state.set_state(Register.location)


@router.message(Register.location, F.location)
async def get_user_location_handler(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(longitude=message.location.longitude, latitude=message.location.latitude)
    data = await state.get_data()
    if await register(data=data, session=session):
        await message.answer(text="You have successfully registered 🎉",
                             reply_markup=user_main_menu)
    else:
        await message.answer(text="Please try again later, something went wrong 😔")

    await state.clear()
