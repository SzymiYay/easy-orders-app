from order_app.order.customer.model import Customer
from order_app.order.product.model import Product, Category
from order_app.order.model import Order
from order_app.data_loader.orders_loader import get_orders

from decimal import Decimal
from datetime import datetime, date

import pytest
import unittest


class TestOrdersLoader(unittest.TestCase):

    @unittest.expectedFailure
    def test_get_orders(self):
        orders = [
            {
                "customer": {
                    "name": "JOHN",
                    "surname": "MAYER",
                    "age": 24,
                    "email": "johnmayer@gmail.com"
                },
                "product": {
                    "name": "LAPTOP",
                    "price": 5300,
                    "category": "A"
                },
                "quantity": 1,
                "order_date": "12-06-2022"
            },
            {
                "customer": {
                    "name": "ANNA",
                    "surname": "SNOW",
                    "age": 36,
                    "email": "ann45snow@gmail.com"
                },
                "product": {
                    "name": "TV",
                    "price": 2400,
                    "category": "A"
                },
                "quantity": 3,
                "order_date": "12-06-2022"
            },
            {
                "customer": {
                    "name": "ALBERT",
                    "surname": "GILBERT",
                    "age": 13,
                    "email": "gilbertgod@gmail.com"
                },
                "product": {
                    "name": "car",
                    "price": 25000,
                    "category": "B"
                },
                "quantity": 2,
                "order_date": "01-06-2021"
            },
            {
                "customer": {
                    "name": "JOHN",
                    "surname": "MAYER",
                    "age": 24,
                    "email": "johnmayer@gmail.com"
                },
                "product": {
                    "name": "LAPTOP",
                    "price": 5300,
                    "category": "C"
                },
                "quantity": 1,
                "order_date": "12-06-2022"
            },
            {
                "customer": {
                    "name": "ANNA",
                    "surname": "SNOW",
                    "age": 36,
                    "email": "ann45snow@gmail.com"
                },
                "product": {
                    "name": "TV",
                    "price": 2400,
                    "category": "C"
                },
                "quantity": 3,
                "order_date": "12-06-2022"
            },
            {
                "customer": {
                    "name": "ALBERT",
                    "surname": "GILBERT",
                    "age": 13,
                    "email": "gilbertgod@gmail.com"
                },
                "product": {
                    "name": "car",
                    "price": 25000,
                    "category": "B"
                },
                "quantity": 2,
                "order_date": "01-01-2021"
            }
        ]
        expected_result = [
            Order(customer=Customer(name='JOHN', surname='MAYER', age=24, email='johnmayer@gmail.com'),
                  product=Product(name='LAPTOP', price=Decimal('5300'), category=Category.A), quantity=1,
                  order_date=date(2022, 6, 12)),
            Order(customer=Customer(name='ANNA', surname='SNOW', age=36, email='ann45snow@gmail.com'),
                  product=Product(name='TV', price=Decimal('2400'), category=Category.A), quantity=3,
                  order_date=date(2022, 6, 12)),
            Order(customer=Customer(name='ALBERT', surname='GILBERT', age=13, email='gilbertgod@gmail.com'),
                  product=Product(name='car', price=Decimal('25000'), category=Category.B), quantity=2,
                  order_date=date(2021, 6, 1)),
            Order(customer=Customer(name='JOHN', surname='MAYER', age=24, email='johnmayer@gmail.com'),
                  product=Product(name='LAPTOP', price=Decimal('5300'), category=Category.C), quantity=1,
                  order_date=date(2022, 6, 12)),
            Order(customer=Customer(name='ANNA', surname='SNOW', age=36, email='ann45snow@gmail.com'),
                  product=Product(name='TV', price=Decimal('2400'), category=Category.C), quantity=3,
                  order_date=date(2022, 6, 12)),
            Order(customer=Customer(name='ALBERT', surname='GILBERT', age=13, email='gilbertgod@gmail.com'),
                  product=Product(name='car', price=Decimal('25000'), category=Category.B), quantity=2,
                  order_date=date(2021, 1, 1))]
        result = get_orders(orders)

        self.assertListEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
