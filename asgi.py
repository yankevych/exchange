from aiogram.dispatcher.webhook import get_new_configured_app
from aiohttp import web
from tbot.views import *

if __name__ == "__main__":
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_PATH)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host='localhost', port=8000)
