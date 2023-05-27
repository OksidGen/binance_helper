import hashlib
import hmac
import os
import time
import urllib.parse

from aiohttp import ClientSession


class BinanceClient:
    _api_key = os.getenv('BINANCE_API_KEY', 'error')
    _secret_key = os.getenv('BINANCE_SECRET_KEY', 'error')
    _endpoints = {
        "NewOrder": {
            "method": "POST",
            "end": "/api/v3/order"
        },
        "CancelAllOpenOrderBySymbol": {
            "method": "DELETE",
            "end": "/api/v3/openOrders"
        },
        "CurrentOpenOrders": {
            "method": "GET",
            "end": "/api/v3/openOrders"
        }
    }
    _base_url = ("https://testnet.binance.vision"
                 if os.getenv("DEBUG", "true").lower() in ("true", "1", "t")
                 else "https://api3.binance.com")

    _session: ClientSession

    def __init__(self):
        self._session = ClientSession(self._base_url)

    async def send_request(self, action: str, **kwargs):
        headers = {
            "X-MBX-APIKEY": self._api_key,
        }

        data_str = urllib.parse.urlencode(kwargs)
        data_str += f"&timestamp={int(time.time() * 1000)}"
        data_str += (
            "&signature=" + hmac.new(
                key=bytearray(self._secret_key, encoding="utf-8"),
                msg=data_str.encode("utf-8"),
                digestmod=hashlib.sha256,
            ).hexdigest()
        )
        response = await self._session.request(
            method=self._endpoints[action]['method'],
            url=f"{self._endpoints[action]['end']}?{data_str}",
            headers=headers
        )

        return await response.json()

    async def close_session(self):
        await self._session.close()
