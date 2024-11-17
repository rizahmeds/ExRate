from django.urls import include, path
from rest_framework import routers

from exchange.views import CurrencyExchangeRateView, CurrencyViewSet


router = routers.DefaultRouter()
router.register(r'currency', CurrencyViewSet)
router.register(r'exchange-rate', CurrencyExchangeRateView)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path(
    #     'exchange-rate/<str:source_currency_code>/<str:from>/<str:to>/',
    #     CurrencyExchangeRateView.as_view(),
    #     name='exchange-rate'
    # ),
]