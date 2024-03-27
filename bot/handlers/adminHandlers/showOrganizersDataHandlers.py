from aiogram import types, Dispatcher

from createBot import db

import filters as f
import keyboards as kb


async def show_list_of_organizers(m: types.Message):
    await m.answer(
        text='Список организаторов:',
        reply_markup=kb.get_list_of_organizers_kb(db.get_list_of_organizers())
    )


async def del_organizer(c: types.CallbackQuery):
    org = c.data.split('_')[1]
    db.del_organizer(org)

    await c.message.edit_reply_markup(
        reply_markup=kb.get_list_of_organizers_kb(db.get_list_of_organizers())
    )
    await c.answer('Организатор успешно удалён')


def register_show_organizers_data_handlers(dp: Dispatcher):
    dp.message.register(show_list_of_organizers, f.TextFilter(''), f.AdminFilter())
    dp.callback_query.register(del_organizer, f.StartsWithFilter('delorg_'), f.AdminFilter())
