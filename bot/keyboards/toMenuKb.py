from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


go_to_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
    ]
)

go_to_menu_reply_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Вернуться в меню')]],
    resize_keyboard=True
)
