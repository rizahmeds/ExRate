from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests
from decimal import Decimal

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return self.code
    
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
        # URL of the external API (CurrencyBeacon in this case)
        url = 'https://api.currencybeacon.com/v1/historical'
        
        # Construct the API query parameters
        params = {
            'base': source_currency.code,  # Assuming the Currency model has a `code` field (e.g. 'USD')
            'symbols': exchanged_currency.code,
            'date': valuation_date,  # The date in the required format
            'api_key': settings.CURRENCY_BEACON_API_KEY  # Store your API key in settings.py
        }

        # Make the API request
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Parse the JSON response and retrieve the exchange rate
            data = response.json()['response']
            # print("data: ", data)
            if 'rates' in data:
                rate_value = Decimal(data['rates'][exchanged_currency.code])
                
                # Store the new exchange rate in the database
                exchange_rate = CurrencyExchangeRate(
                    source_currency=source_currency,
                    exchanged_currency=exchanged_currency,
                    valuation_date=valuation_date,
                    rate_value=rate_value
                )
                exchange_rate.save()
                
                # Return the fetched rate
                return rate_value
            else:
                # Handle error if 'rate' is not in the response data
                raise ValueError("Rate not found in the API response")
        else:
            # Handle error if the API request fails
            raise Exception(f"API request failed with status code {response.status_code}")