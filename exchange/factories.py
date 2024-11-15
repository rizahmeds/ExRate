import factory
from factory.django import DjangoModelFactory

from exchange.models import Currency, CurrencyExchangeRate


class CurrencyFactory(DjangoModelFactory):
    class Meta:
        model = Currency
    #     django_get_or_create = ("email",)

    # email = factory.Faker("email")