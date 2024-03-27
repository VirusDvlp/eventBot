from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_organizer_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Посмотреть список мероприятий')],
        [KeyboardButton(text='Добавить новое мероприятие')]
    ],
    resize_keyboard=True
)
