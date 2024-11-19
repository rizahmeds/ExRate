from datetime import date
from decimal import Decimal
import random
from typing import Optional
from exchange.providers.clients.base import BaseProviderClient, ExchangeRate


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