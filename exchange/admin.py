from django.contrib import admin

from exchange.models import Currency, CurrencyExchangeRate, ExchangeRateProvider

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')

@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('source_currency', 'exchanged_currency', 'rate_value', 'valuation_date')

@admin.register(ExchangeRateProvider)
class ExchangeRateProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'is_active']
    list_editable = ['priority', 'is_active']
    ordering = ['priority']