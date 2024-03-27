from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext

from FSM import EditUserDataFSM
from createBot import db

import keyboards as kb
import filters as f


async def ask_what_edit(m: types.Message):
    user = db.get_user_info(m.from_user.id)
    await m.answer(
        f'Ваш профиль:\nИмя - {user["name"]}\nНомер телефона - {user["phone"]}\n\nВыберите, что хотите редактировать',
        reply_markup=kb.edit_user_data_kb
    )


async def ask_new_data(c: types.CallbackQuery, state: FSMContext):
    what = c.data.split('_')[1]
    if what == 'phone':
        await c.message.answer('Поделитесь своим номером телефона по кнопке ниже', reply_markup=kb.request_phone_kb)
    elif what == 'name':
        await state.set_state(EditUserDataFSM.valueState)
        await state.update_data(key=what)
        await c.message.answer('Введите новое имя', reply_markup=kb.go_to_menu_kb)
    await c.answer()


async def get_new_value(m: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    db.edit_user_data(m.from_user.id, data['key'], m.text[:100])
    await m.answer('Данные успешно изменены')


def register_edit_user_data_handlers(dp: Dispatcher):
    dp.message.register(ask_what_edit, f.TextFilter('Изменить данные профиля'))
    dp.callback_query.register(ask_new_data, f.StartsWithFilter('edit_'))
    dp.message.register(get_new_value, f.StateFilter(EditUserDataFSM.valueState))
