import pytest
from binance_helper.validators import Validator

tested_data = {
    "volume": 10000.0,
    "number": 1,
    "amountDif": 50.0,
    "side": "SELL",
    "priceMin": 200.0,
    "priceMax": 300.0
}


def easy_err_msg(key: str, value) -> str:
    return f'Validate Error: the key [{key}] has an invalid value [{value}]'


def test_check_conditions():
    try:
        Validator.check_conditions(tested_data)
    except Exception:
        assert False

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

    tested_data.clear()
    with pytest.raises(ValueError) as exc:
        Validator.check_conditions(tested_data)
    assert 'Validate Error: not all keys are present' in str(exc.value)
