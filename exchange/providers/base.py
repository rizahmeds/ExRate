from abc import ABC, abstractmethod


class BaseExchangeRateProvider(ABC):
    
    @abstractmethod
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        pass
    
    @abstractmethod
    def get_historical_rates(self, source_currency, exchanged_currencies, date_from, date_to):
        pass