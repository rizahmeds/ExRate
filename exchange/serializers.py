from django.contrib.auth.models import Group, User
from rest_framework import serializers, validators
from django.utils.translation import gettext_lazy as _

from exchange.models import Currency, CurrencyExchangeRate

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'symbol']

class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value']
