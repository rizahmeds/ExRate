# services.py
from typing import Optional, Dict, Type
from django.core.cache import cache
from datetime import date
import logging

from exchange.providers.clients.base import BaseProviderClient
from exchange.providers.clients.currency_beacon import CurrencyBeaconClient
from exchange.providers.clients.mock import MockProviderClient
from exchange.providers.clients.open_exchange_rates import OpenExchangeRatesClient


logger = logging.getLogger(__name__)


class DynamicExchangeService:
    """Service that uses provider configurations from the database"""
    
    PROVIDER_CLASSES: Dict[str, Type[BaseProviderClient]] = {
        'currencybeacon': CurrencyBeaconClient,
        'openexchangerates': OpenExchangeRatesClient,
        'mock': MockProviderClient
    }
    
    def __init__(self):
        self._provider_instances: Dict[int, BaseProviderClient] = {}
        
    def _get_provider_instance(self, provider_config) -> Optional[BaseProviderClient]:
        """Get or create provider instance based on configuration"""
        if provider_config.id not in self._provider_instances:
            provider_class = self.PROVIDER_CLASSES.get(provider_config.provider_class)
            if not provider_class:
                logger.error(f"Unknown provider class: {provider_config.provider_class}")
                return None
                
            try:
                self._provider_instances[provider_config.id] = provider_class(
                    api_key=provider_config.api_key,
                    base_url=provider_config.base_url
                )
            except Exception as e:
                logger.error(f"Failed to initialize provider {provider_config.name}: {str(e)}")
                return None
                
        return self._provider_instances[provider_config.id]

    def _get_cache_key(self, source_currency: str, exchanged_currency: str, 
                       valuation_date: date) -> str:
        """Generate cache key for exchange rate"""
        return f"exchange_rate:{source_currency}:{exchanged_currency}:{valuation_date}"

    def get_exchange_rate(self, source_currency: str, exchanged_currency: str, 
                         valuation_date: date):
        """Get exchange rate trying each active provider in priority order"""
        
        # Check cache first
        cache_key = self._get_cache_key(source_currency, exchanged_currency, valuation_date)
        cached_rate = cache.get(cache_key)
        if cached_rate:
            return cached_rate
        
        from exchange.models import ExchangeRateProvider

        # Get active providers ordered by priority
        active_providers = ExchangeRateProvider.objects.filter(
            is_active=True
        ).order_by('priority')

        for provider_config in active_providers:
            logger.info(f"Attempting to get rate from {provider_config.name}")
            
            provider = self._get_provider_instance(provider_config)
            if not provider:
                continue

            try:
                rate = provider.get_exchange_rate(
                    source_currency, exchanged_currency, valuation_date
                )
                if rate:
                    # Cache successful result for 1 hour
                    cache.set(cache_key, rate, timeout=3600)
                    logger.info(f"Successfully got rate from {provider_config.name}")
                    return rate
                logger.warning(f"No rate available from {provider_config.name}")
            except Exception as e:
                logger.error(f"Error getting rate from {provider_config.name}: {str(e)}")
                continue

        logger.error("Failed to get rate from any provider")
        return None