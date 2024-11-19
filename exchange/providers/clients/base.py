from dataclasses import dataclass
from datetime import date
from decimal import Decimal


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