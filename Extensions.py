import json
import requests
from config import keys
class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
           raise APIException('Невозможно конвертировать одинаковые валюты. Введите значения в правильном формате.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}". Выберите валюту из списка /values.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}". Выберите валюту из списка /values.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}". Введите правильные данные или нажмите /help')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        get_price = json.loads(r.content)[keys[base]]*amount

        return get_price