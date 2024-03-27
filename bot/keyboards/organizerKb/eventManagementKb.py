from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_event_list_kb(events: list, page=0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cur_events = events
    if len(events) > 5:
        cur_events = cur_events[5 * page: 5 * (page + 1)]
    [
        builder.row(InlineKeyboardButton(text=f'{e["title"]} - {e["datetime"]}', callback_data=f'einfo_{e["id"]}'))
        for e in events
    ]

    remain = (page + 1) * 5 - len(cur_events)
    if page > 0:
        builder.button(text='<-', callback_data=f'ehprev_{page}')
    if remain > 5:
        builder.button(text='->', callback_data=f'ehnext_{page}')
    builder.row(InlineKeyboardButton(text=f'Страница: {page + 1}', callback_data=' '))
    return builder.as_markup()


def get_org_event_info_kb(event_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Удалить мероприятие', callback_data=f'delevent_{event_id}')],
            [InlineKeyboardButton(text='Назад к списку мероприятий', callback_data=f'ehprev_{1}')],
        ]
    )


pay_type_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Онлайн', callback_data='pt_0')],
        [InlineKeyboardButton(text='На самом мероприятии', callback_data='pt_1')]
    ]
)
