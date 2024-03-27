from aiogram import types, Dispatcher


from createBot import db
from utils import get_event_info_text

import filters as f
import keyboards as kb


async def show_events(m: types.Message):
    events = db.get_all_events()
    await m.answer(
        'Выберите событие, которое хотите посмотреть',
        reply_markup=kb.get_event_list_kb(events)
    )


async def prev_page(c: types.CallbackQuery):
    events = db.get_all_events()
    page = int(c.data.split('_')[1])
    if page > 0:
        await c.message.edit_reply_markup(
            reply_markup=kb.get_event_list_kb(events, page)
        )
        await c.answer()


async def next_page(c: types.CallbackQuery):
    events = db.get_all_events()
    page = int(c.data.split('_')[1])
    await c.message.edit_reply_markup(
        reply_markup=kb.get_event_list_kb(events, page)
    )
    await c.answer()


async def show_event_info(c: types.CallbackQuery):
    event = c.data.split('_')[1]
    event_info = db.get_event_info(event)
    text = get_event_info_text(event_info, is_for_organizer=False)
    await c.message.answer(
        text=text,
        reply_markup=kb.get_event_info_kb(event)
    )
    await c.answer()


def register_show_events_data_handlers(dp: Dispatcher):
    dp.message.register(show_events, f.TextFilter('Посмотреть список мероприятий'))
    dp.callback_query.register(prev_page, f.StartsWithFilter('ehprev_'))
    dp.callback_query.register(next_page, f.StartsWithFilter('ehnext_'))
    dp.callback_query.register(show_event_info, f.StartsWithFilter('einfo_'))
