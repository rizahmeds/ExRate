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
cd socio
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
5. Create a superuser (admin) account:
```
python manage.py createsuperuser
```
6. Load database with dummy users using management command:
```
python manage.py populate_users
```
7. Run the development server:
```
python manage.py runserver
```

The application should now be running at http://127.0.0.1:8000/admin.

## API Endpoints

| Method   | URL                                      | Description                              |
| -------- | ---------------------------------------- | ---------------------------------------- |
| `POST`   | `/api/currency-rates-list/`              | Service to retrieve a List of currency rates for a specific time period. |
| `POST`   | `/api/convert-amount/`                   | Service that calculates (latest) amount in a currency exchanged into a different currency (currency converter). |
| `GET`    | `/api/currency/`                         | Currency CRUD. |
| `POST`   | `/api/currency/`                         | Add Currency. |


# ExRate Postman Collection
Explore Postman collections for a hands-on, practical approach to using our APIs. These provide an interactive way to explore and test ExRate APIs. They are designed to help you quickly get started.
[Postman Collection Link](ExRateAPI.postman_collection.json)
