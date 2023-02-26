from order_app.validator.text import matches_regex, has_only_upper
from .product.model import Category
from ..logger.model import MyLogger

from typing import Any
from datetime import date


def validate_order_data(order_data: dict[str, Any]) -> bool:
    errors = {
        'name': order_data['customer']['name'],
        'customer': _validate_order_customer(order_data),
        'product': _validate_order_product(order_data),
        'quantity': _validate_order_quantity(order_data),
        'order_date': _validate_order_date(order_data),
    }

    logger_validator = MyLogger.get_logger()

    if len(errors['customer']) != 0 or \
            len(errors['product']) != 0 or \
            len(errors['quantity']) != 0 or \
            len(errors['order_date']) != 0:
        logger_validator.error(', '.join([f'{k}: {v}' for k, v in errors.items()]))
        return False

    return True


def _validate_order_customer(order_date: dict[str, Any]) -> list[str]:
    if 'customer' not in order_date:
        return ['Required']

    errors = []
    order_customer = order_date['customer']
    customer_name = order_customer['name']
    customer_surname = order_customer['surname']
    customer_age = order_customer['age']
    customer_email = order_customer['email']

    if not has_only_upper(customer_name):
        errors.append('Must contain only uppercase letters')

    if not has_only_upper(customer_surname):
        errors.append('Must contain only uppercase letters')

    if customer_age < 18:
        errors.append('Age must be greater than 18')

    if not matches_regex(r'^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$', customer_email):
        errors.append('Incorrect email')

    return errors


def _validate_order_product(order_data: dict[str, Any]) -> list[str]:
    if 'product' not in order_data:
        return ['Required']

    errors = []
    order_product = order_data['product']
    product_name = order_product['name']
    product_price = order_product['price']
    product_category = order_product['category']

    categories = [c.name for c in Category]

    if not has_only_upper(product_name):
        errors.append('Must contain only uppercase letters')

    if product_price < 0:
        errors.append('Price must be positive value')

    if product_category not in categories:
        errors.append(f'Permitted categories {", ".join(categories)}')

    return errors


def _validate_order_quantity(order_data: dict[str, Any]) -> list[str]:
    if 'quantity' not in order_data:
        return ['Required']

    errors = []
    order_quantity = order_data['quantity']

    if order_quantity < 0:
        errors.append('Quantity must be positive value')

    return errors


def _validate_order_date(order_data: dict[str, Any]) -> list[str]:
    if 'order_date' not in order_data:
        return ['Required']

    errors = []
    order_date = order_data['order_date']

    today = date.today()
    date_arr = list(map(int, order_date.split('-')))
    order_date = date(date_arr[2], date_arr[1], date_arr[0])

    if order_date < today:
        errors.append('Date cannot be from the past')

    return errors
