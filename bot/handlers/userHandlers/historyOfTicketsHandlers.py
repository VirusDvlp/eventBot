from aiogram import types, Dispatcher

from createBot import db

import keyboards as kb
import filters as f


async def show_tickets(m: types.Message):
    tickets = db.get_tickets_by_user(m.from_user.id)
    await m.answer(
        'История билетов:',
        reply_markup=kb.get_tickets_list_kb(tickets)
    )


async def prev_page(c: types.CallbackQuery):
    tickets = db.get_all_tickets()
    page = int(c.data.split('_')[1])
    if page > 0:
        await c.message.edit_reply_markup(
            reply_markup=kb.get_tickets_list_kb(tickets, page)
        )
        await c.answer()


async def next_page(c: types.CallbackQuery):
    tickets = db.get_all_tickets()
    page = int(c.data.split('_')[1])
    await c.message.edit_reply_markup(
        reply_markup=kb.get_tickets_list_kb(tickets, page)
    )
    await c.answer()


def register_show_tickets_data_handlers(dp: Dispatcher):
    dp.message.register(show_tickets, f.TextFilter('Посмотреть мои билеты'))
    dp.callback_query.register(prev_page, f.StartsWithFilter('thprev_'))
    dp.callback_query.register(next_page, f.StartsWithFilter('thnext_'))
