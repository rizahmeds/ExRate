from exchange.providers.base import BaseExchangeRateProvider
from exchange.providers.currency_beacon import CurrencyBeaconProvider
from exchange.providers.mock import MockExchangeRateProvider


class Adaptor(CurrencyBeaconProvider, MockExchangeRateProvider):

    def fetch_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        rate_value = self.get_exchange_rate(source_currency, exchanged_currency, valuation_date)
        print("rate_value: ", rate_value)

        return rate_value