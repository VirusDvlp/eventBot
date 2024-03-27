from aiogram import types, Dispatcher

from createBot import db
from utils import get_event_info_text

import keyboards as kb
import filters as f


async def show_list_of_events(m: types.Message):
    org_events = db.get_all_events()
    await m.answer(
        'Выберите событие, которое хотите редактировать',
        reply_markup=kb.get_event_list_kb(org_events)
    )


async def prev_page(c: types.CallbackQuery):
    org_events = db.get_all_events()
    page = int(c.data.split('_')[1])
    if page > 0:
        await c.message.edit_reply_markup(
            reply_markup=kb.get_event_list_kb(org_events, page - 1)
        )
        await c.answer()


async def next_page(c: types.CallbackQuery):
    org_events = db.get_all_events()
    page = int(c.data.split('_')[1])
    await c.message.edit_reply_markup(
        reply_markup=kb.get_event_list_kb(org_events, page + 1)
    )
    await c.answer()


async def show_event_info(c: types.CallbackQuery):
    event = c.data.split('_')[1]
    event_info = db.get_event_info(event)
    text = get_event_info_text(event_info)
    await c.message.edit_text(text=text)
    await c.message.edit_reply_markup(reply_markup=kb.get_org_event_info_kb(event))


async def delete_event(c: types.CallbackQuery):
    event = c.data.split('_')[1]
    db.delete_event(event)
    await c.message.answer('Событие успешно удалено')
    await c.answer()


def register_show_events_data_handlers(dp: Dispatcher):
    dp.message.register(show_list_of_events, f.TextFilter('Посмотреть список мероприятий'), f.AdminFilter())
    dp.callback_query.register(prev_page, f.StartsWithFilter('ehprev_'), f.AdminFilter())
    dp.callback_query.register(next_page, f.StartsWithFilter('ehnext_'), f.AdminFilter())
    dp.callback_query.register(
        show_event_info,
        f.StartsWithFilter('einfo_'),
        f.Or(f.AdminFilter(), f.OrganizerFilter())
    )
    dp.callback_query.register(delete_event, f.StartsWithFilter('delevent_'), f.Or(f.AdminFilter(), f.OrganizerFilter()))
