from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext

import keyboards as kb
import filters as f


async def start_cmd(m: types.Message, state: FSMContext):
    await state.clear()
    await m.answer('Открыто главное меню администратора', reply_markup=kb.main_admin_kb)


async def go_to_menu(c: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await c.message.answer('Открыто главное меню', reply_markup=kb.main_admin_kb)
    await c.answer()


def register_main_admin_handlers(dp: Dispatcher):
    dp.message.register(start_cmd, f.CommandFilter('start'), f.AdminFilter(), f.StateFilter('*'))
    dp.callback_query.register(go_to_menu, f.TextFilter('menu'), f.AdminFilter(), f.StateFilter('*'))
