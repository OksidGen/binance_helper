from aiohttp import web

from binance_helper import server


def test_create_server_with_router():
    s = server.Server()
    assert type(s.app) == web.Application
    assert len(s.app._router.routes()) > 0