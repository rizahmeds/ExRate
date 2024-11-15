import random

from django.db import transaction
from django.core.management.base import BaseCommand

from exchange.factories import CurrencyFactory
from exchange.models import Currency, CurrencyExchangeRate


NUM_USERS = 50


class Command(BaseCommand):
    help = "Generates test data for users..."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Currency]
        for m in models:
            m.objects.exclude(id=456).delete()

        self.stdout.write("Creating new data...")
        # Create dummy users
        for _ in range(NUM_USERS):
            pass
            # role = random.choice([x[0] for x in CustomUser.Types.choices])
            # user = CurrencyFactory(role=role)