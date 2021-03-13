from aiogram import types


async def start_monitoring(bot, r, message):
    """f-n that add user_id to redis and send STOP button"""
    message_id = str(message['from']['id'])

    subscribers = r.get('subscribers')
    if message_id not in subscribers.decode("utf-8"):
        sub_list = ' '.join([subscribers.decode("utf-8"), message_id])
        r.set('subscribers', sub_list)
    else:
        pass
    text = 'start monitoring'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('🛑 STOP'))
    await bot.send_message(message_id, text=text, reply_markup=keyboard)


async def stop_monitoring(bot, r, message):
    """f-n that replace user_id from redis and send START button"""
    message_id = str(message['from']['id'])

    r.delete(f"{message['from']['id']}")   # clear last send msg_id in db

    subscribers = r.get('subscribers')
    if message_id in subscribers.decode("utf-8"):
        sub_list = subscribers.decode("utf-8").replace(message_id, '')
        r.set('subscribers', sub_list)
    else:
        pass
    text = 'stop monitoring'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('💹 START'))
    await bot.send_message(message_id, text=text, reply_markup=keyboard)

