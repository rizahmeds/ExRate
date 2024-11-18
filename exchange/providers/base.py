from abc import ABC, abstractmethod


class BaseExchangeRateProvider(ABC):
    
    @abstractmethod
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        pass