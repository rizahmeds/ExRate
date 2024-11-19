import logging
import requests
from decimal import Decimal
from .base import BaseProviderClient, ExchangeRate


logger = logging.getLogger(__name__)


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