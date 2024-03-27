from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


main_admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Зарегистрировать организатора')],
        [KeyboardButton(text='Посмотреть список мероприятий')],
        [KeyboardButton(text='Добавить новое мероприятие')],
        [KeyboardButton(text='Изменить настройки бота')]
    ],
    resize_keyboard=True
)

edit_bot_data_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Приветсвенное сообщение', callback_data='edit_descr')],
        [InlineKeyboardButton(text='Описание', callback_data='edit_about')]
    ]
)
