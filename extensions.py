import requests
import json
from config import TOKEN_2
from config import exchanges

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")
        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты: {base}!')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')


        url = f"https://api.apilayer.com/exchangerates_data/convert?to={sym_key}&from={base_key}&amount={amount}"

        payload = {}
        headers = {
            "apikey": TOKEN_2
        }

        r = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(r.content)
        result = resp['result']
        return round(result, 2)
