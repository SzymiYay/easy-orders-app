from .customer.model import Customer
from .product.model import Product, Category

from dataclasses import dataclass
from typing import Any
from decimal import Decimal
from datetime import date


@dataclass
class Order:
    customer: Customer
    product: Product
    quantity: int
    order_date: date

    def is_ordered_between(self, date_from: date, date_to: date) -> bool:
        return date_from <= self.order_date <= date_to

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Order':
        order = Order(**data)

        order.customer = Customer(**data['customer'])

        order.product = Product(**data['product'])
        order.product.price = Decimal(data['product']['price'])
        order.product.category = Category[data['product']['category']]

        date_arr = list(map(int, order.order_date.split('-')))
        order.order_date = date(date_arr[2], date_arr[1], date_arr[0])

        return order
