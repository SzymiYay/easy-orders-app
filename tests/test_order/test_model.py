from order_app.order.model import Order
from order_app.order.customer.model import Customer
from order_app.order.product.model import Product, Category

from decimal import Decimal
from datetime import date
import unittest


class TestOrderModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.order = Order(
            customer=Customer(name='JOHN', surname='MAYER', age=24, email='johnmayer@gmail.com'),
            product=Product(name='LAPTOP', price=Decimal('5300'), category=Category.A),
            quantity=1,
            order_date=date(2022, 6, 12)
        )

    def test_is_ordered_between(self):
        result = self.order.is_ordered_between(date(2022, 1, 1), date(2022, 12, 12))
        self.assertTrue(result)

    def test_not_ordered_between(self):
        result = self.order.is_ordered_between(date(2022, 8, 12), date(2022, 12, 12))
        self.assertFalse(result)

    def test_from_dict(self):
        order = {
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
        }
        expected_result = self.order
        result = self.order.from_dict(order)

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
