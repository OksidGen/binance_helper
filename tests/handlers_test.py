import json

import pytest
from aiohttp import web

from binance_helper import handlers


@pytest.fixture
def cli(event_loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/ping', handlers.Handler.ping)
    app.router.add_post('/create_order', handlers.Handler.create_orders)
    app.router.add_get('/get_orders', handlers.Handler.get_orders)
    app.router.add_delete('/delete_orders', handlers.Handler.delete_orders)
    return event_loop.run_until_complete(aiohttp_client(app))


@pytest.mark.asyncio
async def test_ping(cli):
    resp = await cli.get('/ping')
    assert resp.status == 200
    text = await resp.text()
    assert 'pong' in text

expected_result_good = {
    "symbol": "LTCUSDT",
    "orderId": 2812684,
    "type": "LIMIT",
    "side": "SELL",
    "price": "206.10000000",
    "quantity": "9.93115000"
}


@pytest.mark.asyncio
async def test_create_orders_good(cli, mocker):
    data = dict.fromkeys(['volume','number','amountDif','side','priceMin','priceMax'])
    mocker.patch.object(handlers.Service, 'create_orders',
                        return_value=expected_result_good)
    resp_good = await cli.post('/create_order', data=json.dumps(data))
    assert resp_good.status == 200
    result_good = await resp_good.json()
    assert expected_result_good == result_good

@pytest.mark.asyncio
async def test_create_orders_no_data(cli):
    resp_bad = await cli.post('/create_order')
    assert resp_bad.status == 400
    result_bad = await resp_bad.json()
    assert 'error' in result_bad

@pytest.mark.asyncio
async def test_create_orders_bad_data(cli):
    resp_bad = await cli.post('/create_order',data=json.dumps({}))
    assert resp_bad.status == 400
    result_bad = await resp_bad.json()
    assert 'error' in result_bad


@pytest.mark.asyncio
async def test_get_orders(cli, mocker):
    mocker.patch.object(handlers.Service, 'get_orders',
                        return_value=expected_result_good)
    resp = await cli.get('/get_orders')
    assert resp.status == 200
    result = await resp.json()
    assert expected_result_good == result


@pytest.mark.asyncio
async def test_delete_orders(cli, mocker):
    mocker.patch.object(handlers.Service, 'delete_orders',
                        return_value=expected_result_good)
    resp = await cli.delete('/delete_orders')
    assert resp.status == 200
    result = await resp.json()
    assert expected_result_good == result
