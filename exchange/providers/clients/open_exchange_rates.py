from datetime import date
from decimal import Decimal
import logging
from typing import Optional

import requests
from exchange.providers.clients.base import BaseProviderClient, ExchangeRate

logger = logging.getLogger(__name__)


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