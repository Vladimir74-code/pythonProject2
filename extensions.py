# содержит классы и методы
import requests
import json
from config import CRYPTOMPAR_API_KEY

class APIException(Exception):
    pass

class CryptoCurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        if base == quote:
            raise APIException(f'Нельзя указать одинаковые валюты: {base}')

        url = f'https://min-api.cryptocompare.com/data/price'
        parameters = {
            'fsym': base,
            'tsyms': quote,
            'api_key': CRYPTOMPAR_API_KEY
        }

        response = requests.get(url, params=parameters)

        if response.status_code != 200:
            raise APIException(f'Ошибка получения данных: {response.status_code} - {response.text}')

        data = response.json()

        if 'response' in data and not data['response']:
            raise APIException('Ошибка в API: Неверный ответ от сервера')

        if quote not in data:
            raise APIException(f'Валюта {quote} не найдена')

        base_price = data[quote]
        return base_price * amount
