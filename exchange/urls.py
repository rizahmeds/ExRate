from django.urls import include, path
from rest_framework import routers

from exchange.views import CurrencyViewSet

# from users.views import LoginView, SignupView, UserViewSet, FriendshipViewSet

router = routers.DefaultRouter()
router.register(r'currency', CurrencyViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]