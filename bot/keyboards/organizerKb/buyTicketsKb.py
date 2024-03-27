from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_verify_pay_kb(ticket_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Подтвердить оплату', callback_data=f'verify_{ticket_id}')],
            [InlineKeyboardButton(text='Отменить покупку билета', callback_data=f'unverify_{ticket_id}')]
        ]
    )
