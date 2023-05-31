class Validator:
    err_msg_start = 'Validate Error:'

    @staticmethod
    def check_conditions(conditions: dict):
        keys = ('volume', 'number', 'amountDif',
                'side', 'priceMin', 'priceMax')
        if not all(key in conditions for key in keys):
            raise ValueError(
                f'{Validator.err_msg_start} not all keys are present')
        pass

        for key, value in conditions.items():
            err_msg = f'{Validator.err_msg_start} the key [{key}] has an invalid value [{value}]'

            if not key in ('side', 'symbol', 'type', 'timeInForce'):
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
                f"{Validator.err_msg_start} priceMin must be less then priceMax")

        conditions['symbol'] = conditions.get('symbol', 'LTCUSDT')
        conditions['type'] = "LIMIT"
        conditions['timeInForce'] = "GTC"

    @staticmethod
    async def check_binance_conditions(conditions: dict, send_req):
        response_filtres = await send_req(action='ExchangeInfo', symbol=conditions['symbol'])
        response_avgPrice = await send_req(action='AvgPrice', symbol=conditions['symbol'])

        filtres = response_filtres['symbols'][0]['filters']

        conditions['stepSize'] = int(filtres[1]['stepSize'].find('1'))-1

        avgPrice = float(response_avgPrice['price'])
        if conditions['side'] == 'SELL':
            priceMax = float(filtres[5]['askMultiplierUp']) * avgPrice
            priceMin = float(filtres[5]['askMultiplierDown']) * avgPrice
        else:
            priceMax = float(filtres[5]['bidMultiplierUp']) * avgPrice
            priceMin = float(filtres[5]['bidMultiplierDown']) * avgPrice

        if conditions['priceMax'] > priceMax:
            conditions['priceMax'] = priceMax
        if conditions['priceMin'] < priceMin:
            conditions['priceMin'] = priceMin

        if conditions['priceMax'] < conditions['priceMin']:
            raise ValueError(
                f"{Validator.err_msg_start} From Binance - invalid price values")
