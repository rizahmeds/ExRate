from rest_framework import viewsets
from rest_framework import filters
from exchange.models import Currency, CurrencyExchangeRate
from exchange.serializers import CurrencyExchangeRateSerializer, CurrencySerializer
from rest_framework.response import Response
from rest_framework import status


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows currencies to be viewed or edited.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [filters.SearchFilter]

    search_fields = ['code', 'name']


class CurrencyExchangeRateView(viewsets.ModelViewSet):

    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateSerializer
    
    def create(self, request, *args, **kwargs):
        # print("request.data: ", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        # print("Data: ", data)

        source_currency = data.get("source_currency")
        exchanged_currency = data.get("exchanged_currency")
        valuation_date = data.get("valuation_date")
        res = CurrencyExchangeRate.get_exchange_rate(source_currency, exchanged_currency, valuation_date)
        
        return Response(res, status=status.HTTP_201_CREATED)