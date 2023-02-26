from .data_loader.json.json_service import load_from_json
from .data_loader.orders_loader import get_orders
from .order.service import OrdersService
from .logger.model import CustomFormatter, MyLogger

from typing import Final
from datetime import date

import logging


def main() -> None:
    """LOGGING"""
    logger = MyLogger.get_logger()

    """APP"""
    logger.warning('STARTING APP')
    FILENAME: Final[str] = 'order_app/data/orders.json'

    orders_data = load_from_json(FILENAME)
    logger.info('Successfully loaded orders data')

    orders = get_orders(orders_data)
    logger.info('Successfully loaded orders')

    order_service = OrdersService(orders)
    logger.info('Successfully created OrdersService')

    logger.debug('Full price between dates')
    print(order_service.get_full_price_between(date(2021, 1, 1), date(2022, 12, 12)))

    logger.debug('Most expensive product for each category')
    print(order_service.get_most_expensive_product_for_each_category())

    logger.debug('Most expensive product for each category 2')
    print(order_service.get_most_expensive_product_for_each_category2)

    logger.debug('Profile for each client')
    print(order_service.get_profile_for_each_client())

    logger.debug('Date with most and least orders')
    print(order_service.get_date_with_most_and_least_orders()[0])
    print(order_service.get_date_with_most_and_least_orders()[1])

    logger.debug('Client with most expensive order')
    print(order_service.get_client_with_most_expensive_order())

    logger.debug('Full price with discounts')
    print(order_service.get_full_price_with_discounts())

    logger.debug('Clients with products quantity at least 2')
    print(order_service.get_clients_with_products_quantity_at_least(2))

    logger.debug('Most common product for each category')
    print(order_service.get_most_common_product_category())

    logger.debug('Monthly statistics')
    print(order_service.get_monthly_statistics())

    logger.debug('Monthly statistics with category')
    print(order_service.get_monthly_statistics_with_category())

    logger.warning('ENDING APP')
