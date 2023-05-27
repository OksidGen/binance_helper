import asyncio

from aiohttp import web

from binance_helper import handlers


class Server:

    def __init__(self):
        self.app = web.Application()
        self.app.add_routes(Server._create_routes())

    @staticmethod
    def _create_routes() -> list[web.RouteDef]:
        routes = [
            web.get('/ping', handlers.Handler.ping),
            web.post('/create_orders', handlers.Handler.create_orders),
            web.get('/get_orders', handlers.Handler.get_orders),
            web.delete('/delete_orders', handlers.Handler.delete_orders)
        ]
        return routes

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        host = 'localhost'
        port = 8080
        site = web.TCPSite(runner, host, port)
        await site.start()
        print('Server started')
        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            print('Server closed')
        finally:
            await handlers.Service.binance_cli.close_session()
            await runner.cleanup()
