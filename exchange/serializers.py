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


class ConvertAmountSerializer(CurrencyExchangeRateSerializer):

    source_currency = serializers.ReadOnlyField(source='source_currency.code')
    exchanged_currency = serializers.ReadOnlyField(source='exchanged_currency.code')
    # amount = serializers.DecimalField(decimal_places=6, max_digits=18)
    amount = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'exchanged_currency', 'valuation_date', 'amount']
    
    def get_amount(self, obj):
        request = self.context['request']
        amount = request.query_params['amount']
        return (float(amount) * float(obj.rate_value))
