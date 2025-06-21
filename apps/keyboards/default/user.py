from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_number_share = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Share phone number ☎️", request_contact=True)
    ]], resize_keyboard=True, one_time_keyboard=True
)

location_share = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Share location 🌏", request_location=True)
    ]], resize_keyboard=True, one_time_keyboard=True
)

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Menu 🍴")
        ],
        [
            KeyboardButton(text="Basket 🛒"),
            KeyboardButton(text="My orders 📝")
        ],
        [
            KeyboardButton(text="Send feedback ✍️"),
            KeyboardButton(text="Settings ⚙️"),
        ]
    ], resize_keyboard=True
)

back_user_main_menu = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Back ⬅️")
    ]], resize_keyboard=True
)
