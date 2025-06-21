from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from apps.keyboards.default.user import back_user_main_menu, user_main_menu
from apps.states.user import Feedback
from core.config import DEVELOPER

router = Router()


@router.message(F.text == "Send feedback ✍️")
async def send_feedback_handler(message: types.Message, state: FSMContext):
    text = "Please enter your message in one text"
    await message.answer(text=text, reply_markup=back_user_main_menu)

    await state.set_state(Feedback.feedback)


@router.message(Feedback.feedback)
async def get_feedback_handler(message: types.Message, state: FSMContext, bot: Bot):
    # user = get_user(chat_id=message.chat.id)
    user = []
    feedback = f"""
User: {message.from_user.mention_html(f'{user[1]}')}
Feedback: {message.text}
    """
    await bot.send_message(text=feedback, chat_id=DEVELOPER)

    text = "Your feedback is sent to admins ✅"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.clear()

    await state.set_state(Feedback.feedback)
