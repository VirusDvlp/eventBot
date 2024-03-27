from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Посмотреть список мероприятий')],
        [KeyboardButton(text='Посмотреть мои билеты')],
        [KeyboardButton(text='Изменить данные профиля')],
        [KeyboardButton(text='Реферальная система')]
    ],
    resize_keyboard=True
)

request_phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить свой номер телефона', request_contact=True)]
    ],
    resize_keyboard=True
)

edit_user_data_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Номер телефона', callback_data='edit_phone')],
        [InlineKeyboardButton(text='Имя', callback_data='edit_name')]
    ]
)

sub_on_channel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Канал', url='https://t.me/ebbclub')],
        [InlineKeyboardButton(text='Я подписался', callback_data='chnl_sub')]
    ]
)
