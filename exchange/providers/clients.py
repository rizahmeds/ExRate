# services.py
from dataclasses import dataclass
import random
from typing import Optional, Dict, Type
from django.core.cache import cache
from decimal import Decimal
from datetime import date
import logging
import requests

logger = logging.getLogger(__name__)

@dataclass
class ExchangeRate:
    source_currency: str
    exchanged_currency: str
    rate_value: Decimal
    valuation_date: date
    provider_name: str 

    
class BaseProviderClient:
    """Base class for provider clients"""
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

class CurrencyBeaconClient(BaseProviderClient):

    def get_exchange_rate(self, source_currency: str, exchanged_currency: str, valuation_date):
        try:
            params = {
                "api_key": self.api_key,
                "base": source_currency,
                "symbols": exchanged_currency,
                "date": valuation_date
            }
            print( "params: ", params )
            request_url = f"{self.base_url}/historical"
            response = requests.get(request_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()['response']
                return ExchangeRate(
                    source_currency=source_currency,
                    exchanged_currency=exchanged_currency,
                    rate_value=Decimal(str(data['rates'][exchanged_currency])),
                    valuation_date=valuation_date,
                    provider_name="CurrencyBeacon"
                )
            logger.warning(f"CurrencyBeacon API returned status code {response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error fetching from CurrencyBeacon: {str(e)}")
            return None

class OpenExchangeRatesClient(BaseProviderClient):

    def get_exchange_rate(self, source_currency: str, exchanged_currency: str, 
                         valuation_date: date) -> Optional[ExchangeRate]:
        try:
            params = {
                "app_id": self.api_key,
                "base": source_currency,
                "symbols": exchanged_currency
            }
            # print( "OpenExchangeRatesClient params: ", params )
            request_url = f"{self.base_url}/historical/{valuation_date}.json"
            response = requests.get(request_url, params=params,timeout=5)
            # print("response: ", response)
            if response.status_code == 200:
                data = response.json()
                return ExchangeRate(
                    source_currency=source_currency,
                    exchanged_currency=exchanged_currency,
                    rate_value=Decimal(str(data['rates'][exchanged_currency])),
                    valuation_date=valuation_date,
                    provider_name="OpenExchangeRates"
                )
            logger.warning(f"OpenExchangeRates API returned status code {response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error fetching from OpenExchangeRates: {str(e)}")
            return None

class MockProviderClient(BaseProviderClient):
    
    def get_exchange_rate(self, source_currency: str, exchanged_currency: str, 
                         valuation_date: date) -> Optional[ExchangeRate]:
        rate = Decimal(str(random.uniform(0.5, 2.0)))
        return ExchangeRate(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            rate_value=rate.quantize(Decimal("0.000001")),
            valuation_date=valuation_date,
            provider_name="MockProvider"
        )