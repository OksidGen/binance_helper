import pytest

from binance_helper.services import Service
from binance_helper.validators import Validator


def easy_err_msg(key: str, value) -> str:
    return f'Validate Error: the key [{key}] has an invalid value [{value}]'


def test_check_conditions():
    tested_data = {
        "volume": 10000.0,
        "number": 1,
        "amountDif": 50.0,
        "side": "SELL",
        "priceMin": 200.0,
        "priceMax": 300.0
    }
    tested_data.update({'volume': 'test'})
    with pytest.raises(ValueError) as exc:
        Validator.check_conditions(tested_data)
    assert f"{easy_err_msg('volume','test')} - must be a number" in str(exc.value)

    tested_data.update({'volume': 1, 'number': 0})
    with pytest.raises(ValueError) as exc:
        Validator.check_conditions(tested_data)
    assert f"{easy_err_msg('number',0)} - must be greater than zero" in str(exc.value)

    tested_data.update({'number': -1})
    with pytest.raises(ValueError) as exc:
        Validator.check_conditions(tested_data)
    assert f"{easy_err_msg('number',-1)} - must be positive" in str(exc.value)

    tested_data.update({'number': 1, 'side': 'test'})
    with pytest.raises(ValueError) as exc:
        Validator.check_conditions(tested_data)
    assert f"{easy_err_msg('side','test')} - acceptable values: \"SELL\", \"BUY\"" in str(exc.value)

    tested_data.update({'side': 'SELL', 'priceMin': 2, 'priceMax': 1})
    with pytest.raises(ValueError) as exc:
        Validator.check_conditions(tested_data)
    assert 'Validate Error: priceMin must be less then priceMax' in str(
        exc.value)

    tested_data.update({'priceMin': 0})
    try:
        Validator.check_conditions(tested_data)
    except Exception:
        assert False

    tested_data.clear()
    with pytest.raises(ValueError) as exc:
        Validator.check_conditions(tested_data)
    assert 'Validate Error: not all keys are present' in str(exc.value)


@pytest.mark.asyncio
async def test_check_binance_condtitions(mocker):
    tested_data = {
        "volume": 10000.0,
        "number": 1,
        "amountDif": 50.0,
        "side": "SELL",
        "priceMin": 200.0,
        "priceMax": 300.0,
    }
    mocked_response = {
        "price": "89.23762654",
        "symbols": [
            {
                "filters": [
                    {
                        "filterType": "PRICE_FILTER",
                        "minPrice": "0.01000000",
                        "maxPrice": "100000.00000000",
                        "tickSize": "0.01000000"
                    },
                    {
                        "filterType": "LOT_SIZE",
                        "minQty": "0.00001000",
                        "maxQty": "9000.00000000",
                        "stepSize": "0.00001000"
                    },
                    {
                        "filterType": "ICEBERG_PARTS",
                        "limit": 10
                    },
                    {
                        "filterType": "MARKET_LOT_SIZE",
                        "minQty": "0.00000000",
                        "maxQty": "1000.00000000",
                        "stepSize": "0.00000000"
                    },
                    {
                        "filterType": "TRAILING_DELTA",
                        "minTrailingAboveDelta": 10,
                        "maxTrailingAboveDelta": 2000,
                        "minTrailingBelowDelta": 10,
                        "maxTrailingBelowDelta": 2000
                    },
                    {
                        "filterType": "PERCENT_PRICE_BY_SIDE",
                        "bidMultiplierUp": "5",
                        "bidMultiplierDown": "0.2",
                        "askMultiplierUp": "5",
                        "askMultiplierDown": "0.2",
                        "avgPriceMins": 1
                    },
                ],
            }
        ]
    }

    Validator.check_conditions(tested_data)
    mocker.patch.object(Service.binance_cli, 'send_request',
                        return_value=mocked_response)

    try:
        await Validator.check_binance_conditions(tested_data, Service.binance_cli.send_request)
    except Exception:
        assert False

    tested_data.update({'side': 'BUY', 'priceMax': 10000, 'priceMin': 0})
    try:
        await Validator.check_binance_conditions(tested_data, Service.binance_cli.send_request)
    except Exception:
        assert False

    tested_data.update({'priceMin':10000,'priceMax':20000})
    with pytest.raises(ValueError) as exc:
        await Validator.check_binance_conditions(tested_data,Service.binance_cli.send_request)
    assert 'From Binance - invalid price values' in str(exc.value)