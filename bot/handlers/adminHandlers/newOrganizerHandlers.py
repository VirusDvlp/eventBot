from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram import F

from FSM import NewOrganizerFSM
from createBot import db

import filters as f
import keyboards as kb


async def ask_user(m: types.Message, state: FSMContext):
    await state.set_state(NewOrganizerFSM.contactState)
    await m.answer('Поделитесь контактом организатора', reply_markup=kb.req_contact_kb)


async def ask_name(m: types.Message, state: FSMContext):
    await state.set_state(NewOrganizerFSM.nameState)
    contact = m.user_shared
    await state.update_data(user_id=contact.user_id)
    await m.answer('Введите имя организатора(до 100 символов)', reply_markup=kb.main_admin_kb)


async def register_organizer(m: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    db.new_organizer(data['user_id'], m.text[:100])
    await m.answer('Организато успешно зарегистрирован')


def register_new_organizer_handlers(dp: Dispatcher):
    dp.message.register(ask_user, f.TextFilter('Зарегистрировать организатора'), f.AdminFilter())
    dp.message.register(
        ask_name,
        F.user_shared,
        f.StateFilter(NewOrganizerFSM.contactState)
    )
    dp.message.register(
        register_organizer,
        f.StateFilter(NewOrganizerFSM.nameState)
    )
