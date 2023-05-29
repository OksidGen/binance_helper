import json

from aiohttp import web

from binance_helper.services import Service
from binance_helper.validators import Validator


class Handler:
    @staticmethod
    async def ping(request):
        return web.Response(text='pong')

    @staticmethod
    async def create_orders(request):
        try:
            conditions = await request.json()
            Validator.check_conditions(conditions)
        except json.decoder.JSONDecodeError:
            return web.json_response({'error': 'problem with json decoding, incorrect data'}, status=400)
        except ValueError as err:
            return web.json_response({'error': str(err)}, status=400)

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
