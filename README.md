# ExRate
Django Rest Framework based Backend of a web platform that allows users to calculate currency exchange rates.

# Features

- Currency rates list
- Convert amount
- Currency CRUD

# Installation

1. Clone the repository:
```
git clone https://github.com/rizahmeds/ExRate.git
cd ExRate
```
2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Apply the database migrations:
```
python manage.py migrate
```
5. To load data:
```
python manage.py loaddata exchange/fixtures/Currency.json --app exchange.Currency
python manage.py loaddata exchange/fixtures/CurrencyExchangeRate.json --app exchange.CurrencyExchangeRate
python manage.py loaddata exchange/fixtures/ExchangeRateProvider.json --app exchange.ExchangeRateProvider

```
6. Create a superuser (admin) account:
```
python manage.py createsuperuser
```
7. Run the development server:
```
python manage.py runserver
```

The application should now be running at http://127.0.0.1:8000/admin.

## API Endpoints

| Method   | URL                            | Parameters           | Description                              |
| -------- | ------------------------------ | -------------------- | ---------------------------------------- |
| `GET`    | `/api/v1/currency/`            |                      | Retrieve Currencies. |
| `POST`   | `/api/v1/currency/`            | symbol, name, code   | Create Currency. |
| `PATCH`  | `/api/v1/currency/{id}/`       | symbol/name/code     | Update Currency. |
| `DELETE` | `/api/v1/currency/{id}/`       |                      | Delete Currency. |
| `GET`    | `/api/v1/currency_rates_list/` | source_currency, date_from, date_to | List of currency rates. |
| `GET`    | `/api/v1/convert_amount/`      | source_currency, exchanged_currency, amount | Calculates amount |



# ExRate Postman Collection
Explore Postman collections for a hands-on, practical approach to using our APIs. These provide an interactive way to explore and test ExRate APIs. They are designed to help you quickly get started.
[Postman Collection Link](ExRateAPI.postman_collection.json)
