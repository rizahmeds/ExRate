from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator

from exchange.providers import Adaptor
from exchange.providers.service import DynamicExchangeService
from exchange.providers.currency_beacon import CurrencyBeaconProvider


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return f"{self.code} - {self.name}"


class ExchangeRateProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    base_url = models.URLField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1)])
    api_key = models.CharField(max_length=100, blank=True)
    provider_class = models.CharField(
        max_length=50,
        choices=[
            ('currencybeacon', 'Currency Beacon'),
            ('openexchangerates', 'Open Exchange Rates'),
            ('mock', 'Mock Provider')
        ]
    )

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"{self.name} (Priority: {self.priority})"
    

class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18, null=True, blank=True)

    class Meta:
        verbose_name = _("Currency Exchange Rate")
        verbose_name_plural = _("Currency Exchange Rates")
        unique_together = ('source_currency', 'exchanged_currency', 'valuation_date')

    def __str__(self):
        return '{}: {}'.format(self.source_currency, self.exchanged_currency)

    @staticmethod
    def get_exchange_rate(source_currency, exchanged_currency, valuation_date):
        """
        Retrieve exchange rate from the database or external API if not found.
        """
        try:
            # First, try to fetch the exchange rate from the database
            exchange_rate = CurrencyExchangeRate.objects.get(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=valuation_date
            )
            return exchange_rate.rate_value
        
        except ObjectDoesNotExist:
            # If the exchange rate is not found in the database, fetch it from the external API
            base = Currency.objects.get(pk=source_currency)
            symbols = Currency.objects.get(pk=exchanged_currency)
            return CurrencyExchangeRate.fetch_and_store_exchange_rate(base, symbols, valuation_date)

    @staticmethod
    def fetch_and_store_exchange_rate(source_currency, exchanged_currency, valuation_date):
        """
        Fetch exchange rate from the external API and store it in the database.
        """
        try:
            for provider in ExchangeRateProvider.objects.all():
                # Initialize the service
                service = DynamicExchangeService()

                exchange_rate = service.get_exchange_rate(source_currency.code, exchanged_currency.code, valuation_date)
                print("service rate_value: ", exchange_rate.rate_value)
                rate = exchange_rate.rate_value
                # rate = CurrencyBeaconProvider(provider.api_key).get_exchange_rate(
                #     source_currency.code, exchanged_currency.code, valuation_date
                # )
                if rate is not None:
                    print("rate_value: ", rate)

                    exchange_rate = CurrencyExchangeRate(
                        source_currency=source_currency,
                        exchanged_currency=exchanged_currency,
                        valuation_date=valuation_date,
                        rate_value=rate
                    )
                    exchange_rate.save()
                    return
                
            raise Exception(f"Provider not able to fetch rate.")
        
        except Exception as e:
            # Handle error if the API request fails
            raise Exception(f"API request failed: {e.__str__()}")
