import stripe
from config.settings import STRIPE_API_KEY
import requests

stripe.api_key = STRIPE_API_KEY

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Получить курс через бесплатный API exchangerate-api.com"""
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][to_currency]

def convert_rub_to_dollars(amount):
    """ Конвертация рублей в доллары"""
    rate = get_exchange_rate("RUB", "USD")

    return int(rate * amount)

def create_stripe_price(amount, product):
    """ Создание цены в Страйпе """
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product=product
    )

def create_stripe_product(amount):
    """ Создание продукта в Страйпе """
    stripe.api_key = STRIPE_API_KEY
    return stripe.Product.create(name="Product")

def create_stripe_session(price):
    """ Создание сессии на оплату в страйпе """
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8080/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    ).to_dict()
    return session.get('id'), session.get('url')
