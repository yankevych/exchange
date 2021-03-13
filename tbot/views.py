import asyncio
import uvloop
import os

from redis import Redis
from .bot_tools import start_monitoring, stop_monitoring
from loguru import logger
from aiogram import Bot, Dispatcher, types


from pyngrok import ngrok

server_url = ngrok.connect(addr=8000).public_url
logger.info('server_url', server_url.replace('http', 'https'))

API_TOKEN = os.getenv('TOKEN')
WEBHOOK_URL = server_url.replace('http', 'https')
WEBHOOK_PATH = f'/{API_TOKEN}'

uvloop.install()
loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, loop=loop, parse_mode='HTML')
dp = Dispatcher(bot)


# r = Redis(host='localhost', port=6379, db=0)    # local setting
r = Redis(host='redis', username='default', password='redis_pass_', port=6379, db=0)


@dp.message_handler(commands=['start'])
async def raw221(message: types.Message):
    """first start button handler"""
    await start_monitoring(bot, r, message)


@dp.message_handler(lambda message: message.text)
async def raw222(message: types.Message):
    """handler that take all messages from user/ STOP and START command"""

    if message.text == '🛑 STOP':
        await stop_monitoring(bot, r, message)

    elif message.text == '💹 START':
        await start_monitoring(bot, r, message)


async def on_startup(dp):
    # set hook and log status
    res = await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH, max_connections=100, drop_pending_updates=True)
    logger.info(res)

    # clean redis db
    r.set('subscribers', '')


async def on_shutdown(dp):
    await bot.delete_webhook()  # del hook
    r.close()   # close redis db


