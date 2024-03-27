from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_event_info_kb(event_id) -> InlineKeyboardMarkup:
    buy_bt = InlineKeyboardButton(text='Купить билет', callback_data=f'bevent_{event_id}')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [buy_bt]
        ]
    )


def get_i_paid_kb(event_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Я оплатил', callback_data=f'paid_{event_id}')]
        ]
    )
