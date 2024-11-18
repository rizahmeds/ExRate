from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from exchange.models import Currency, CurrencyExchangeRate

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'symbol']

class CurrencyExchangeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyExchangeRate
        fields = '__all__'


class CurrencyRatesListSerializer(CurrencyExchangeRateSerializer):

    source_currency = serializers.ReadOnlyField(source='source_currency.code')

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'valuation_date', 'rate_value']
