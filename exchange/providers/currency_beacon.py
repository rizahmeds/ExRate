import requests
from decimal import Decimal
from .base import BaseExchangeRateProvider

class CurrencyBeaconProvider(BaseExchangeRateProvider):
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.currencybeacon.com/v1"

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        params = {
            'api_key': self.api_key,
            'base': source_currency,
            'symbols': exchanged_currency,
            'date': valuation_date
        }
        
        response = requests.get(f"{self.base_url}/historical", params=params)
        if response.status_code == 200:
            data = response.json()['response']
            return Decimal(str(data['rates'][exchanged_currency]))
        return None