import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base} друг в друга')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Проверьте правильность ввода валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Проверьте правильность ввода валюты {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Проверьте правильность ввода количества валюты {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total = json.loads(r.content)[keys[quote]] * amount
        return total
