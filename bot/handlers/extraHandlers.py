from aiogram import types, Dispatcher

import filters as f


async def answer_callback(c: types.CallbackQuery):
    await c.answer()


def register_extra_handlers(dp: Dispatcher):
    dp.callback_query.register(answer_callback, f.StateFilter('*'))
