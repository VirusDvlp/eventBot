from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext

from FSM import EditBotDataFSM

import config as c
import keyboards as kb
import filters as f


async def ask_what_edit(m: types.Message):
    await m.answer('Выберите, что хотите редактировать', reply_markup=kb.edit_bot_data_kb)


async def ask_value(c: types.CallbackQuery, state: FSMContext):
    what = c.data.split('_')[1]
    await state.set_state(EditBotDataFSM.valueState)
    await state.update_data(key=what)
    await c.message.answer('Введите новое значение', reply_markup=kb.go_to_menu_kb)
    await c.answer()


async def edit_bot_data(m: types.Message, state: FSMContext):
    data = await state.get_data()
    what = data['key']
    await state.clear()
    if what == 'about':
        await m.bot.set_my_description(m.text)
    await m.answer('Данные бота успешно изменено', reply_markup=kb.main_admin_kb)


def register_edit_bot_data_handlers(dp: Dispatcher):
    dp.message.register(ask_what_edit, f.TextFilter('Изменить настройки бота'), f.AdminFilter())
    dp.callback_query.register(ask_value, f.StartsWithFilter('edit_'), f.AdminFilter())
    dp.message.register(edit_bot_data, f.StateFilter(EditBotDataFSM.valueState))
