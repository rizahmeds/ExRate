from rest_framework import permissions, viewsets
from rest_framework import filters
from exchange.models import Currency
from exchange.serializers import CurrencySerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [filters.SearchFilter]

    search_fields = ['code', 'name']