from django.contrib.auth.models import Group, User
from rest_framework import serializers, validators
from django.utils.translation import gettext_lazy as _

from exchange.models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'symbol']
