from datetime import datetime, timedelta
from rest_framework import viewsets
from rest_framework.views import APIView

# from rest_framework import filters
from exchange.models import Currency, CurrencyExchangeRate
from exchange.serializers import (
    ConvertAmountSerializer,
    CurrencyExchangeRateSerializer,
    CurrencyRatesListSerializer,
    CurrencySerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from exchange.utils import get_missing_dates

class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows currencies to be viewed or edited.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


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


class ConvertAmount(GenericAPIView):

    serializer_class = ConvertAmountSerializer

    def get(self, request, *args, **kwargs):
        print(request.query_params)

        source_currency = request.query_params.get('source_currency')
        exchanged_currency = request.query_params.get('exchanged_currency')
        amount = request.query_params.get('amount')
        valuation_date = datetime.today().strftime('%Y-%m-%d')

        # Start with base queryset
        try:
            source_currency_code = Currency.objects.get(code=source_currency).pk
            exchanged_currency_code = Currency.objects.get(code=exchanged_currency).pk
            CurrencyExchangeRate.get_exchange_rate(source_currency_code, exchanged_currency_code, valuation_date)
        except Exception as e:
            print("Exception: ", e.__str__())

        # Start with base queryset
        queryset = self.get_queryset()
       
        queryset = queryset.filter(
            source_currency__code__iexact=source_currency,
            exchanged_currency__code__iexact=exchanged_currency,
            valuation_date=valuation_date,
        )
        print("queryset: ", queryset)
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        """
        Get optimized queryset with select_related
        """
        return CurrencyExchangeRate.objects.select_related().all()

class CurrencyRatesList(GenericAPIView):

    serializer_class = CurrencyRatesListSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            # Get query parameters
            # print(request.query_params)
            source_currency = request.query_params.get('source_currency')
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            
            if not all([source_currency, date_from, date_to]):
                return Response(
                    {'error': 'Missing required parameters'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            delta = timedelta(days=1)
            start_date = datetime.strptime(date_from, "%Y-%m-%d").date()
            end_date = datetime.strptime(date_to, "%Y-%m-%d").date()

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
                    valuation_date__gte=date_from, 
                    valuation_date__lte=date_to
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