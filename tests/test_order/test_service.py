from order_app.order.customer.model import Customer
from order_app.order.product.model import Product, Category
from order_app.order.model import Order
from order_app.order.service import OrdersService

from decimal import Decimal
from datetime import date

import pytest
import unittest

class TestOrdersService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.orders = OrdersService([
            Order(customer=Customer(name='JOHN', surname='MAYER', age=24, email='johnmayer@gmail.com'),
                  product=Product(name='LAPTOP', price=Decimal('5300'), category=Category.A),
                  quantity=1,
                  order_date=date(2022, 6, 12)),
            Order(customer=Customer(name='ANNA', surname='SNOW', age=36, email='ann45snow@gmail.com'),
                  product=Product(name='TV', price=Decimal('2400'), category=Category.A),
                  quantity=3,
                  order_date=date(2022, 6, 12)),
            Order(customer=Customer(name='ALBERT', surname='GILBERT', age=13, email='gilbertgod@gmail.com'),
                  product=Product(name='car', price=Decimal('25000'), category=Category.B),
              quantity=2,
              order_date=date(2021, 6, 1)),
        Order(customer=Customer(name='JOHN', surname='MAYER', age=24, email='johnmayer@gmail.com'),
              product=Product(name='LAPTOP', price=Decimal('5300'), category=Category.C),
              quantity=1,
              order_date=date(2022, 6, 12)),
        Order(customer=Customer(name='ANNA', surname='SNOW', age=36, email='ann45snow@gmail.com'),
              product=Product(name='TV', price=Decimal('2400'), category=Category.C),
              quantity=3,
              order_date=date(2022, 6, 12)),
        Order(customer=Customer(name='ALBERT', surname='GILBERT', age=13, email='gilbertgod@gmail.com'),
              product=Product(name='car', price=Decimal('25000'), category=Category.B),
              quantity=2,
              order_date=date(2021, 1, 1))
    ])

    def test_get_full_price_in_range(self):
        expected_result = 125000
        result = self.orders.get_full_price_between(date(2021, 1, 1), date(2022, 12, 12))

        self.assertEqual(result, expected_result)

    def test_get_full_price_in_range_no_items(self):
        expected_result = 0
        result = self.orders.get_full_price_between(date(2000, 1, 1), date(2000, 12, 12))

        self.assertEqual(result, expected_result)

    def test_incorrect_dates(self):
        with self.assertRaises(ValueError) as e:
            self.orders.get_full_price_between(date(2000, 12, 12), date(2000, 1, 1))

        self.assertEqual('Incorrect date', str(e.exception))

    def test_get_most_expensive_product_for_each_category(self):
        expected_result = {
            Category.A: Product(name='LAPTOP', price=Decimal('5300'), category=Category.A),
            Category.B: Product(name='car', price=Decimal('25000'), category=Category.B),
            Category.C: Product(name='LAPTOP', price=Decimal('5300'), category=Category.C)
        }
        result = self.orders.get_most_expensive_product_for_each_category()

        self.assertEqual(result, expected_result)

    def test_get_profile_each_client(self):
        expected_result = {
            'JOHN MAYER': [Product(name='LAPTOP', price=Decimal('5300'), category=Category.A),
                           Product(name='LAPTOP', price=Decimal('5300'), category=Category.C)],
            'ANNA SNOW': [Product(name='TV', price=Decimal('2400'), category=Category.A),
                          Product(name='TV', price=Decimal('2400'), category=Category.C)],
            'ALBERT GILBERT': [Product(name='car', price=Decimal('25000'), category=Category.B),
                               Product(name='car', price=Decimal('25000'), category=Category.B)]
        }
        result = self.orders.get_profile_for_each_client()

        self.assertEqual(result, expected_result)

    def test_get_date_with_most_and_least_orders(self):
        expected_result = ([date(2022, 6, 12)], [date(2021, 6, 1), date(2021, 1, 1)])
        result = self.orders.get_date_with_most_and_least_orders()

        self.assertEqual(result, expected_result)

    def test_get_client_with_most_expensive_order(self):
        expected_result = Customer(name='ALBERT', surname='GILBERT', age=13, email='gilbertgod@gmail.com')
        result = self.orders.get_client_with_most_expensive_order()

        self.assertEqual(result, expected_result)

    def test_get_full_price_with_discounts(self):
        expected_result = {
            'JOHN MAYER': Decimal('4986.7700'),
            'ANNA SNOW': Decimal('7200'),
            'ALBERT GILBERT': Decimal('47045.0000')
        }
        result = self.orders.get_full_price_with_discounts()

        self.assertDictEqual(result, expected_result)

    def test_get_clients_with_products_quantity_at_least(self):
        expected_result = {'ANNA SNOW': 3, 'ALBERT GILBERT': 2}
        result = self.orders.get_clients_with_products_quantity_at_least(2)

        self.assertDictEqual(result, expected_result)

    def test_get_most_common_product_category(self):
        expected_result = [Category.A, Category.B, Category.C]
        result = self.orders.get_most_common_product_category()

        self.assertListEqual(result, expected_result)

    def test_get_monthly_statistics(self):
        expected_result = [('June', 5), ('January', 1)]
        result = self.orders.get_monthly_statistics()

        self.assertListEqual(result, expected_result)

    def test_get_monthly_statistics_with_category(self):
        expected_result = {
            'June': {Category.A: ['LAPTOP', 'TV'], Category.B: 'car', Category.C: ['LAPTOP', 'TV']},
            'January': {Category.B: 'car'}
        }
        result = self.orders.get_monthly_statistics_with_category()

        self.assertDictEqual(result, expected_result)
