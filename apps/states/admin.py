from aiogram.fsm.state import State, StatesGroup


class CategoryAdd(StatesGroup):
    name_uz = State()
    name_ru = State()
    name_en = State()
