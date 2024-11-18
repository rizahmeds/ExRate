from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from exchange.models import CurrencyExchangeRate

def get_missing_dates(from_date: str, to_date: str):
    # Convert string dates to datetime objects
    from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    # Generate a set of all dates within the specified range
    all_dates = {from_date + timedelta(days=x) for x in range((to_date - from_date).days + 1)}
    print("all_dates: ", all_dates)
    # Query the database for valuated dates within the range
    valued_dates_query = CurrencyExchangeRate.objects.filter(
        valuation_date__range=(from_date, to_date)
    )

    print("valued_dates_query: ", valued_dates_query)

    # Convert query result to a set of dates
    valued_dates = {entry['date_only'] for entry in valued_dates_query}

    # Find missing dates
    missing_dates = all_dates - valued_dates

    return missing_dates