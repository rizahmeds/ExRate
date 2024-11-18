from datetime import datetime, timedelta
from rest_framework import viewsets
from rest_framework.views import APIView

# from rest_framework import filters
from exchange.models import Currency, CurrencyExchangeRate
from exchange.serializers import CurrencyExchangeRateSerializer, CurrencyRatesListSerializer, CurrencySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from django_filters import rest_framework as filters

from exchange.utils import get_missing_dates

class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows currencies to be viewed or edited.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    # filter_backends = [filters.SearchFilter]

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


class CurrencyExchangeRateFilter(filters.FilterSet):
    source_currency = filters.CharFilter(field_name='source_currency__code', lookup_expr='iexact')
    from_date = filters.DateFilter(field_name='valuation_date', lookup_expr='gte')
    to_date = filters.DateFilter(field_name='valuation_date', lookup_expr='lte')

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'valuation_date']


class CurrencyRatesList(GenericAPIView):

    serializer_class = CurrencyRatesListSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            # Get query parameters
            # print(request.query_params)
            source_currency = request.query_params.get('source_currency')
            from_date = request.query_params.get('from_date')
            to_date = request.query_params.get('to_date')
            
            delta = timedelta(days=1)
            start_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(to_date, "%Y-%m-%d").date()

            while start_date <= end_date:
                try:
                    source_currency_code = Currency.objects.get(code=source_currency).pk
                    exchanged_currency_code = Currency.objects.get(code="USD").pk
                    CurrencyExchangeRate.get_exchange_rate(source_currency_code, exchanged_currency_code, start_date)
                except Exception as e:
                    print("Exception: ", e.__str__())
                
                start_date += delta

            # Start with base queryset
            queryset = self.get_queryset()

            # Apply filters
            if source_currency:
                queryset = queryset.filter(
                    source_currency__code__iexact=source_currency,
                    exchanged_currency__code__iexact="USD",
                    valuation_date__gte=from_date, 
                    valuation_date__lte=to_date
                )

            serializer = self.get_serializer(queryset, many=True)
            # print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        """
        Get optimized queryset with select_related
        """
        return CurrencyExchangeRate.objects.select_related().all()