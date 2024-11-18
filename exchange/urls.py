from django.urls import include, path
from rest_framework import routers

from exchange.views import ConvertAmount, CurrencyExchangeRateView, CurrencyRatesList, CurrencyViewSet


router = routers.DefaultRouter()
router.register(r'currency', CurrencyViewSet)
router.register(r'exchange-rate', CurrencyExchangeRateView)
# router.register(r'currency-rates-list', CurrencyRatesList, basename='CurrencyRatesList')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('currency-rates-list/', CurrencyRatesList.as_view(), name='currency-rates-list'),
    path('convert-amount/', ConvertAmount.as_view(), name='convert-amount'),

]
