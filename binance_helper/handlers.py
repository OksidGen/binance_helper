from binance_helper.services import Service
from aiohttp import web


class Handler:
    @staticmethod
    async def ping(request):
        return web.Response(text='pong')

    @staticmethod
    async def create_orders(request):
        try:
            conditions = await request.json()
        except Exception:
            return web.json_response({'error':'no json data'},status=400)
        
        keys = ('volume','number','amountDif','side','priceMin','priceMax')
        if not all(key in conditions for key in keys):
            return web.json_response({'error':'not all keys were transferred'}, status=400)
        
        response = await Service.create_orders(conditions)

        return web.json_response(response, status=200)

    @staticmethod
    async def get_orders(request):
        response = await Service.get_orders()

        return web.json_response(response, status=200)

    @staticmethod
    async def delete_orders(request):
        response = await Service.delete_orders()

        return web.json_response(response, status=200)
