import requests
import os
import uvloop

from loguru import logger
from datetime import datetime
from aiogram import Bot
from redis import Redis
from .celery import app
from aiogram.utils.exceptions import ChatIdIsEmpty, ChatNotFound

MAIN_URL = 'https://coinpay.org.ua/api/v1/exchange_rate'
API_TOKEN = os.getenv('TOKEN')

uvloop.install()
loop = uvloop.new_event_loop()

bot = Bot(token=API_TOKEN, loop=loop, parse_mode='HTML')


@app.task
def main_currency():
    """main f-n -- engine of the update currency"""
    r = Redis(host='localhost', port=6379, db=0)

    subscribers = r.get('subscribers')
    logger.info(subscribers)
    if subscribers:
        response = requests.get(url=MAIN_URL)
        data = response.json()['rates']
        text = f'<u>LAST UPDATE: {datetime.now():%Y-%m-%d -- %H:%M:%S}</u>\n\n'

        for i in sorted(data, key=lambda key: key['pair']):     # sorted Alphabetical
            if i['pair'] in ['BTC_ETH', 'ETH_BTC', 'BTC_USDT', 'ETH_UAH', 'USDT_UAH', 'ETH_USDT', 'BTC_UAH']:
                text += f"<b>{i['pair']}</b> -- {i['price']}\n"
        list_to_send = subscribers.decode("utf-8").split()
        logger.info(list_to_send)

        loop.run_until_complete(send(r, list_to_send, text))    # async run send f-n
    else:
        pass
    r.close()


async def send(r, list_, text):
    """send monitoring to user"""
    for id_ in list_:
        try:
            message_id = r.get(f'{id_}')    # if TRUE > it not the first msg and I can EDIT it
            if message_id:
                message = await bot.edit_message_text(text=text, chat_id=id_, message_id=message_id.decode("utf-8"))
            else:   # if FALSE > it's the first message
                message = await bot.send_message(id_, text=text)
            r.set(f'{id_}', f'{message.message_id}')    # save message ID to db and then can edit it
        except ChatIdIsEmpty:
            pass
        except ChatNotFound:
            pass
