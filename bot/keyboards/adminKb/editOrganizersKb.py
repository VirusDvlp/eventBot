from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_list_of_organizers_kb(organizers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    [
        builder.row(
            InlineKeyboardButton(text=o['name'], callback_data=f'org_{o["id"]}'),
            InlineKeyboardButton(text=' /\\', callback_data=f'delorg_{o["id"]}')
        )

        for o in organizers
     ]
    return builder.as_markup()


req_contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Поделиться контактом', request_user=KeyboardButtonRequestUser(request_id=1))
        ]
    ],
    resize_keyboard=True
)
