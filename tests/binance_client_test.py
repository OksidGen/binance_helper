import hmac
import time

import pytest
from aioresponses import aioresponses

from binance_helper import binance_client


@pytest.mark.asyncio
async def test_send_request(mocker):
    binance = binance_client.BinanceClient()
    expected_result = {"test": "test"}
    url = f"{binance._endpoints['NewOrder']['end']}?test=test&timestamp=1000&signature=sign"
    with aioresponses() as m:
        m.post(url, payload=expected_result)

        mocker.patch.object(time, 'time', return_value=1)
        mocker.patch.object(hmac.HMAC, 'hexdigest', return_value='sign')

        result = await binance.send_request('NewOrder', test='test', sign=True)

        assert expected_result == result
        m.assert_called_once_with(url=url, method='post', headers={
                                  "X-MBX-APIKEY": binance._api_key})

    await binance.close_session()
