from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import re

from FSM import NewEventFSM
from createBot import db
from utils import encode_datetime

import keyboards as kb
import filters as f


async def ask_title(m: types.Message, state: FSMContext):
    await state.set_state(NewEventFSM.titleState)
    await m.answer('Введите название мероприятия(до 100 символов)', reply_markup=kb.go_to_menu_kb)


async def ask_descr(m: types.Message, state: FSMContext):
    await state.update_data(title=m.text[:100])
    await state.set_state(NewEventFSM.descrState)
    await m.answer('Введите описание мероприятия')


async def ask_datetime(m: types.Message, state: FSMContext):
    await state.update_data(descr=m.text[:499])
    await state.set_state(NewEventFSM.datetimeState)
    await m.answer('Введите дату и время мероприятия(до 500 символов)')


async def ask_address(m: types.Message, state: FSMContext):
    expr = r'(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.]20\d\d ([01][0-9]|2[0-3]):[0-5][0-9]'
    if re.findall(expr, m.text):
        await state.update_data(datetime=encode_datetime(m.text))
        await state.set_state(NewEventFSM.addressState)
        await m.answer('Введите адрес мероприятия(до 100 символов)')
    else:
        await m.answer('Дата введена неверно')


async def ask_members_number(m: types.Message, state: FSMContext):
    await state.update_data(address=m.text[:100])
    await state.set_state(NewEventFSM.membersNumberState)
    await m.answer('Введите количество мест на мероприятии')


async def ask_ticket_price(m: types.Message, state: FSMContext):
    try:
        await state.update_data(members_number=int(m.text))
    except ValueError:
        await m.answer('Нужно ввести натуральное число!')
        return None

    await state.set_state(NewEventFSM.priceState)
    await m.answer('Введите цену билета на мероприятие')


async def ask_pay_type(m: types.Message, state: FSMContext):
    try:
        await state.update_data(ticket_price=int(m.text))
    except ValueError:
        await m.answer('Нужно ввести натуральное число!')
        return None
    await state.set_state(NewEventFSM.payTypeState)
    await m.answer('Выберите тип оплаты билета на меорприятие', reply_markup=kb.pay_type_kb)


async def ask_requisites(c: types.CallbackQuery, state: FSMContext):
    pt = c.data.split('_')[1]
    await state.update_data(pay_type=pt)
    if pt == '0':
        await state.set_state(NewEventFSM.requisitesState)
        await c.message.answer('Введите реквизиты, по которым будет производится оплата(до 120 символов)')
    else:
        s_data = await state.get_data()
        await state.clear()
        db.add_event(**s_data, org_id=c.from_user.id)
        await c.message.answer('Мероприятие успешно добавлено')
    await c.answer()


async def add_event(m: types.Message, state: FSMContext):
    s_data = await state.get_data()
    await state.clear()
    db.add_event(**s_data, requisites=m.text[:120], org_id=m.from_user.id)
    await m.answer('Мероприятие успешно добавлено')


def register_new_event_handlers(dp: Dispatcher):
    dp.message.register(ask_title, f.TextFilter('Добавить новое мероприятие'), f.Or(f.AdminFilter(), f.OrganizerFilter()))
    dp.message.register(ask_descr, f.StateFilter(NewEventFSM.titleState))
    dp.message.register(ask_datetime, f.StateFilter(NewEventFSM.descrState))
    dp.message.register(ask_address, f.StateFilter(NewEventFSM.datetimeState))
    dp.message.register(ask_members_number, f.StateFilter(NewEventFSM.addressState))
    dp.message.register(ask_ticket_price,f.StateFilter(NewEventFSM.membersNumberState))
    dp.message.register(ask_pay_type, f.StateFilter(NewEventFSM.priceState))
    dp.callback_query.register(ask_requisites, f.StartsWithFilter('pt_'), f.StateFilter(NewEventFSM.payTypeState))
    dp.message.register(add_event, f.StateFilter(NewEventFSM.requisitesState))
