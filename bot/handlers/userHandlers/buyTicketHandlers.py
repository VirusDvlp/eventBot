from aiogram import types, Dispatcher

from createBot import db

import keyboards as kb
import filters as f


async def send_requisites(c: types.CallbackQuery):
    event = c.data.split('_')[1]
    event_info = db.get_event_info(event)
    if event_info['status'] == 1 or event_info['members'] != event_info['members_number']:
        if event_info['pay_type'] == 0:
            keyboard = kb.get_i_paid_kb(event)
            ref_info = db.get_referal_data(c.from_user.id)
            mess_text = f'''Реквизиты на покупку билете:\n{event_info["requisites"]}\nПосле того, как оплатите по ним,
нажмите на кнопку \"Я оплатил\"'''
            if ref_info['bonus'] >= event_info['ticket_price']:
                mess_text += '\nВы также можете оплатить билет бонусамии, нажав на кнопку \"Оплатить бонусами\"'
                keyboard.inline_keyboard.append(
                    [types.InlineKeyboardButton(text='Оплатить бонусами', callback_data=f'bpaid_{event}')]
                )
            await c.message.answer(mess_text, reply_markup=keyboard)
        elif event_info['pay_type'] == 1:
            db.new_ticket(db.get_user_info(c.from_user.id)['id'], event)
            await c.message.answer('Билет успешно зарезервирован, оплата будет производится на самом мероприятии')
    else:
        await c.message.delete_reply_markup()
        await c.message.answer('На данное мероприятие уже нельзя купить билеты')
    await c.answer()


async def pay_by_bonus(c: types.CallbackQuery):
    event = c.data.split('_')[1]
    event_info = db.get_event_info(event)
    if event_info['status'] == 1 and event_info['members'] != event_info['members_number']:
        ref_info = db.get_referal_data(c.from_user.id)
        if ref_info['bonus'] >= event_info['ticket_price']:
            db.plus_bonus(c.from_user.id, -event_info['ticket_price'])
            if ref_info['referal_to']:
                db.plus_bonus(ref_info['referal_to'], int(event_info['ticket_price'] * 0.05))
            db.new_ticket(ref_info['id'], event, 1)
            await c.answer('Вы успешно оплатили билет бонусами')
        else:
            await c.answer('Недостаточно бонусов на счет')
    else:
        await c.message.delete_reply_markup()
        await c.answer('На данное мероприятие уже нельзя купить билет')


async def send_to_organizer_for_verification(c: types.CallbackQuery):
    event = c.data.split('_')[1]
    event_info = db.get_event_info(event)
    if event_info['status'] == 1 or event_info['members'] == event_info['members_number']:
        user = db.get_user_info(c.from_user.id)
        ticket = db.new_ticket(user['id'], event)
        await c.bot.send_message(
            int(event_info['org_user_id']),
            f'''Подтвердите оплату от пользователя:\n{user["name"]}\n@{user["username"]}
На реквизиты{event_info["requsites"]}, на сумму: {event_info["tikcet_price"]}''',
            reply_markup=kb.get_verify_pay_kb(ticket)
        )
        await c.answer('Ожидайте подтверждение оплаты от организатора')
    else:
        await c.message.delete_reply_markup()
        await c.answer('На данное мероприятие уже нельзя купить билеты')


def register_buy_ticket_handlers(dp: Dispatcher):
    dp.callback_query.register(send_requisites, f.StartsWithFilter('bevent_'))
    dp.callback_query.register(pay_by_bonus, f.StartsWithFilter('bpaid_'))
    dp.callback_query.register(send_to_organizer_for_verification, f.StartsWithFilter('paid_'))
