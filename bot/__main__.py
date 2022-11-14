import asyncio

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from bot.handlers.start import router
from bot.config_reader import config


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(router)
    try:
        await bot.set_webhook(
            url=config.url_domain + config.url_path,
            drop_pending_updates=True,
            allowed_updates=dp.resolve_used_update_types()
        )
        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.url_path)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=config.server_host, port=config.server_port)
        await site.start()

        await asyncio.Event().wait()
    finally:
        await bot.session.close()


asyncio.run(main())