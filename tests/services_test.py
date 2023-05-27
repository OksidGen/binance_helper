import pytest

from binance_helper import services


@pytest.mark.asyncio
async def test_make_orders_good(mocker):
    testing_data = {
        "volume": 10000.0,
        "number": 5,
        "amountDif": 50.0,
        "side": "SELL",
        "priceMin": 200.0,
        "priceMax": 300.0
    }
    expected_result = {
        "Successfully created": [
            {
                "symbol": "LTCUSDT",
                "orderId": 2812684,
                "type": "LIMIT",
                "side": "SELL",
                "price": "206.10000000",
                "quantity": "9.93115000"
            }
        ] * 5,
        'Errors': []
    }

    mock_send_request = {
        "symbol": "LTCUSDT",
        "orderId": 2812684,
        "orderListId": -1,
        "clientOrderId": "FY1BxBXQnjcfXEIygwgcqo",
        "transactTime": 1685118637602,
        "price": "206.10000000",
        "origQty": "9.93115000",
        "executedQty": "0.00000000",
        "cummulativeQuoteQty": "0.00000000",
        "status": "NEW",
        "timeInForce": "GTC",
        "type": "LIMIT",
        "side": "SELL",
        "workingTime": 1685118637602,
        "fills": [],
        "selfTradePreventionMode": "NONE"
    }

    mocker.patch.object(services.BinanceClient, 'send_request',
                        return_value=mock_send_request)

    result = await services.Service.create_orders(testing_data)
    assert result == expected_result


@pytest.mark.asyncio
async def test_make_orders_error(mocker):
    testing_data = {
        "volume": 10000.0,
        "number": 1,
        "amountDif": 50.0,
        "side": "SELL",
        "priceMin": 10000.0,
        "priceMax": 11000.0
    }

    mock_send_request = {
        "code": -1013,
        "msg": "Filter failure: PERCENT_PRICE_BY_SIDE"
    }

    expected_result = {
        "Successfully created": [],
        "Errors": [mock_send_request]
    }

    mocker.patch.object(services.BinanceClient, 'send_request',
                        return_value=mock_send_request)

    result = await services.Service.create_orders(testing_data)
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_orders(mocker):
    expected_result = {
        "Your orders": [],
        "Errors": []
    }
    mock_send_request = []
    mocker.patch.object(services.BinanceClient, 'send_request',return_value=mock_send_request)
    result = await services.Service.get_orders()
    assert expected_result == result

@pytest.mark.asyncio
async def test_delete_orders(mocker):
    expected_result = {
        "Successfully deleted": [],
        "Errors": []
    }
    mock_send_request = []
    mocker.patch.object(services.BinanceClient, 'send_request',return_value=mock_send_request)
    result = await services.Service.delete_orders()
    assert expected_result == result
