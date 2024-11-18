import random
from datetime import date, timedelta
from decimal import Decimal
from .base import BaseExchangeRateProvider

class MockExchangeRateProvider(BaseExchangeRateProvider):
    
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        # Generate deterministic but random-looking rate based on inputs
        seed = int(f"{ord(source_currency[0])}{ord(exchanged_currency[0])}{valuation_date.toordinal()}")
        random.seed(seed)
        rate = random.uniform(0.5, 2.0)
        return Decimal(str(rate)).quantize(Decimal("0.000001"))