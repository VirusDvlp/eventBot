from aiogram import types, Dispatcher

from createBot import db

import keyboards as kb
import filters as f


async def show_list_of_events(m: types.Message):
    org_events = db.get_events_by_organizer(m.from_user.id)
    await m.answer(
        'Выберите событие, которое хотите редактировать',
        reply_markup=kb.get_event_list_kb(org_events)
    )


async def prev_page(c: types.CallbackQuery):
    org_events = db.get_events_by_organizer(c.from_user.id)
    page = int(c.data.split('_')[1])
    if page > 0:
        await c.message.edit_reply_markup(
            reply_markup=kb.get_event_list_kb(org_events, page - 1)
        )
        await c.answer()


async def next_page(c: types.CallbackQuery):
    org_events = db.get_events_by_organizer(c.from_user.id)
    page = int(c.data.split('_')[1])
    await c.message.edit_reply_markup(
        reply_markup=kb.get_event_list_kb(org_events, page + 1)
    )
    await c.answer()


def register_show_events_data_handlers(dp: Dispatcher):
    dp.message.register(show_list_of_events, f.TextFilter('Посмотреть список мероприятий'), f.OrganizerFilter())
    dp.callback_query.register(prev_page, f.StartsWithFilter('ehprev_'), f.OrganizerFilter())
    dp.callback_query.register(next_page, f.StartsWithFilter('ehhext_'), f.OrganizerFilter())
