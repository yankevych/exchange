import nest_asyncio

from loguru import logger
from tbot.views import *
from aiogram.utils.executor import start_webhook
from pyngrok import ngrok

nest_asyncio.apply()    # for correct start loop for start_webhook

server_url = ngrok.connect(addr=8000).public_url
logger.info(server_url.replace('http', 'https'))

API_TOKEN = os.getenv('TOKEN')
WEBHOOK_URL = server_url.replace('http', 'https')
WEBHOOK_PATH = f'/{API_TOKEN}'


async def on_startup(dp):
    # set hook and log status
    set_hook_status = await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH, max_connections=100, drop_pending_updates=True)
    logger.info(set_hook_status)

    # clean redis db
    r.set('subscribers', '')


async def on_shutdown(dp):
    await bot.delete_webhook()  # del hook
    r.close()   # close redis db

start_hook_status = start_webhook(
    dispatcher=dp,
    webhook_path=WEBHOOK_PATH,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host='127.0.0.1',
    port=8000,
)
logger.info(start_hook_status)
