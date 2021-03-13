import os

from redis import Redis
from .bot_tools import start_monitoring, stop_monitoring
from aiogram import Bot, Dispatcher, types


API_TOKEN = os.getenv('TOKEN')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

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


