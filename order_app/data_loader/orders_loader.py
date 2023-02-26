from ..order.model import Order
from ..order.validator import validate_order_data

from typing import Any


def get_orders(order_data: list[dict[str, Any]]) -> list[Order]:
    return [Order.from_dict(order) for order in order_data if validate_order_data(order)]
