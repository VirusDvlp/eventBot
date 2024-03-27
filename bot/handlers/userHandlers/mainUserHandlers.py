from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.deep_linking import decode_payload

from createBot import db

import keyboards as kb
import filters as f


async def start_cmd(m: types.Message, state: FSMContext):
    await state.clear()
    user_id = m.from_user.id
    if db.get_user_info(user_id):
        await m.answer('Открыто главное меню пользователя', reply_markup=kb.main_user_kb)
    else:
        db.register_user(user_id, m.from_user.first_name[:100], m.from_user.username)
        await m.answer(
            'Вам неообходимо зарегистрироваться, нажмите на кнопку ниже, чтобы отправить свой номер телефона',
            reply_markup=kb.request_phone_kb
        )


async def ref_start_cmd(m: types.Message, state: FSMContext, command):
    user_id = m.from_user.id
    if command:
        ref_id = decode_payload(command.args)
        if ref_id:
            if ref_id != str(user_id):
                if db.get_referal_data(ref_id):
                    db.register_user(user_id, m.from_user.first_name, m.from_user.username, ref_id)
                    await m.answer(
                        'Чтобы пользоваться ботом вам неообходимо подпистаться на канал',
                        reply_markup=kb.sub_on_channel_kb
                    )
            else:
                await m.answer('Нельзя регистрироваться по своей собственной реферальной ссылке!')


async def check_sub(c: types.CallbackQuery):
    if not db.get_user_info(c.from_user.id)['phone']:
        if await c.bot.get_chat_member(-1002062568489, c.from_user.id):
            await c.message.answer(
                'Отлично! Теперь вам нужно отправить свой номер телефона, сделайте это по кнопке ниже',
                reply_markup=kb.request_phone_kb
            )
    await c.answer()


async def finish_register(m: types.Message):
    phone = m.contact.phone_number
    user = db.get_user_info(m.from_user.id)
    db.edit_user_data(m.from_user.id, 'phone', phone)
    await m.answer('Ваш номер успешно верифицирован, регистрация завершена!', reply_markup=kb.main_user_kb)
    if not user['phone']:
        if user['referal_to']:
            try:
                await m.bot.send_message(
                    f'''По вашей реферальной ссылке зарегистрировался пользователь - {user["name"]}.
    Теперь вы будете получать бонусы с его покупок'''
                )
            except Exception:
                    pass
        if not user['username']:
            await m.answer(
                '''Предупреждение!!\n У вас не указано имя пользователя в вашем телеграмм аккаунте.
Настоятельно рекомендуем указать его, чтобы вы могли корректно работать с нашим сервисом.'''
            )


async def go_to_menu(c: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await c.message.answer('Открыто главное меню', reply_markup=kb.main_user_kb)
    await c.answer()


def register_main_user_handlers(dp: Dispatcher):
    dp.message.register(start_cmd, f.CommandFilter('start'), f.StateFilter('*'))
    dp.message.register(ref_start_cmd, Command('start'))
    dp.message.register(finish_register, f.ContentTypeFilter(types.ContentType.CONTACT))
    dp.callback_query.register(check_sub, f.StartsWithFilter('chnl_sub'))
    dp.callback_query.register(go_to_menu, f.TextFilter('menu'), f.StateFilter('*'))
