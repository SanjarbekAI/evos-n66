from aiogram import Router, F, types

router = Router()


@router.message(F.text.in_(["Menu 🍴", "Menyu 🍴"]))
async def user_menu_handler(message: types.Message):
    text = "User menu is tapped"
    await message.answer(text=text)
