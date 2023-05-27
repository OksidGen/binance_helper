import asyncio
from random import uniform

from binance_helper.binance_client import BinanceClient


class Service:
    binance_cli = BinanceClient()

    @staticmethod
    async def create_orders(conditions: dict):
        tasks = []
        average_volume = conditions["volume"] / conditions["number"]
        remained_volume = conditions["volume"]

        for i in range(conditions["number"]):
            price = round(
                uniform(conditions["priceMin"], conditions["priceMax"]), 2)
            volume = (round(average_volume + (-1) ** i * uniform(0, conditions["amountDif"]), 2)
                      if i < 4
                      else round(remained_volume, 2)
                      )
            remained_volume -= volume
            quantity = round(volume / price, 5)

            tasks.append(
                asyncio.create_task(
                    Service.binance_cli.send_request(
                        action='NewOrder',
                        symbol='LTCUSDT',
                        side=conditions["side"],
                        type='LIMIT',
                        timeInForce='GTC',
                        price=price,
                        quantity=quantity
                    )
                )
            )

        results = await asyncio.gather(*tasks)

        return brush_results('Successfully created', results)

    @staticmethod
    async def get_orders():
        results = await Service.binance_cli.send_request(action='CurrentOpenOrders', symbol='LTCUSDT')

        return brush_results('Your orders', results)

    @staticmethod
    async def delete_orders():
        results = await Service.binance_cli.send_request(action='CancelAllOpenOrderBySymbol', symbol='LTCUSDT')

        return brush_results('Successfully deleted', results)


def brush_results(msg: str, results: list) -> dict:
    clear_res = {
        msg: [],
        "Errors": []
    }
    for res in results:
        if 'code' not in res:
            clear_res[msg].append({
                'symbol': res['symbol'],
                'orderId': res['orderId'],
                'type': res['type'],
                'side': res['side'],
                'price': res['price'],
                'quantity': res['origQty']
            })
        else:
            clear_res['Errors'].append(res)

    return clear_res
