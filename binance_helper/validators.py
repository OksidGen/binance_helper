class Validator:
    @staticmethod
    def check_conditions(conditions: dict):
        err_msg_start = 'Validate Error:'

        keys = ('volume', 'number', 'amountDif',
                'side', 'priceMin', 'priceMax')
        if not all(key in conditions for key in keys):
            raise ValueError(f'{err_msg_start} not all keys are present')
        pass

        for key, value in conditions.items():
            err_msg = f'{err_msg_start} the key [{key}] has an invalid value [{value}]'

            if not key in ('side', 'symbol'):
                try:
                    v = float(value)
                except ValueError:
                    raise ValueError(f'{err_msg} - must be a number')
                if v < 0:
                    raise ValueError(
                        f'{err_msg} - must be positive')
                if key in ('volume', 'number'):
                    if v == 0:
                        raise ValueError(
                            f'{err_msg} - must be greater than zero')

            else:
                if key == 'side' and value not in ('SELL', 'BUY'):
                    raise ValueError(
                        f'{err_msg} - acceptable values: "SELL", "BUY"')

        if float(conditions['priceMin']) > float(conditions['priceMax']):
            raise ValueError(
                f"{err_msg_start} priceMin must be less then priceMax")

        conditions['symbol'] = conditions.get('symbol', 'LTCUSDT')
