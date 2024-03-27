from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_tickets_list_kb(tickets: list, page=0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cur_tickets = tickets
    if len(tickets) > 5:
        cur_tickets = cur_tickets[5 * page: 5 * (page + 1)]
    [
        builder.row(InlineKeyboardButton(text=f'{e["title"]} - {e["datetime"]}', callback_data=f'tinfo_{e["id"]}'))
        for e in cur_tickets
    ]

    remain = (page + 1) * 5 - len(cur_tickets)
    if page > 0:
        builder.button(text='<-', callback_data=f'thprev_{page}')
    if remain > 5:
        builder.button(text='->', callback_data=f'thnext_{page}')
    builder.row(InlineKeyboardButton(text=f'Страница: {page + 1}', callback_data=' '))
    return builder.as_markup()
