from .model import Order
from .product.model import Category, Product
from .customer.model import Customer
from ..data_loader.json.json_service import save_to_json

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from collections import defaultdict


@dataclass
class OrdersService:
    orders: list[Order]

    def client_and_price(self) -> dict[Customer, Decimal]:
        return {f'{o.customer.name} {o.customer.surname}': o.product.price * o.quantity for o in self.orders}

    def get_full_price_between(self, date_from: date, date_to: date) -> Decimal:
        """
        Obliczenie ceny wszystkich produktów, które zamówiono w przedziale czasowym <d1, d2>,
        gdzie d1 oraz d2 to podane np. jako argument metody obiekty typu LocalDate.
        """
        if date_from > date_to:
            raise ValueError('Incorrect date')

        return sum([order.quantity * order.product.price
                    for order in self.orders
                    if order.is_ordered_between(date_from, date_to)])

    def get_most_expensive_product_for_each_category(self) -> dict[Category, Product]:
        """
        Wyznaczenie dla każdej kategorii produktu o największej cenie.

        #todo czy mozna uzyc tutaj defultdict?
        #todo która wersja funkcji lepsza?
        """
        grouped_by_category = {}

        for c in Category:
            grouped_by_category[c] = [o.product for o in self.orders if c == o.product.category]

        return {key: max(value, key=lambda p: p.price) if len(value) != 0 else None
                for key, value in grouped_by_category.items()}

    def get_most_expensive_product_for_each_category2(self) -> dict[Category, Product]:
        grouped_by_category = {}

        for c in Category:
            grouped_by_category[c] = sorted(
                [o.product for o in self.orders if c == o.product.category], key=lambda o: o.product.price, reverse=True
            )

        return {key: value[0] if len(value) != 1 else None
                for key, value in grouped_by_category.items()}

    def get_profile_for_each_client(self) -> dict[Customer, list[Product]]:
        """
        Przygotowanie dla każdego klienta zestawienia wszystkich produktów, które zamówił
        """
        client_and_product = defaultdict(list)

        for c in self.orders:
            client_and_product[f"{c.customer.name} {c.customer.surname}"].append(c.product)

        return dict(client_and_product)

    def get_date_with_most_and_least_orders(self) -> tuple[date, date]:
        """
        Wyznaczenie daty, dla której złożono najwięcej zamówień oraz daty dla której złożono najmniej zamówień.

        #todo czy mozna skrócić kod?
        """
        grouped_by_date = defaultdict(list)
        grouped_by_no_of_orders = defaultdict(list)

        for order in self.orders:
            grouped_by_date[order.order_date].append(order)

        for order_date, orders in grouped_by_date.items():
            grouped_by_no_of_orders[len(orders)].append(order_date)

        return (
            max(dict(grouped_by_no_of_orders).items(), key=lambda pair: pair[0])[1],
            min(dict(grouped_by_no_of_orders).items(), key=lambda pair: pair[0])[1]
        )

    def get_client_with_most_expensive_order(self) -> Customer:
        """
        Wyznacz informację o kliencie, który zapłacił najwięcej za złożone zamówienia.
        """
        return max(self.orders, key=lambda o: o.product.price * o.quantity).customer

    def get_full_price_with_discounts(self) -> dict[str, Decimal]:
        """
        Zakładamy, że wszystkie zamówienia, których data realizacji jest nie później
        niż 2 dni od daty aktualnej dostają 2% rabat. Zamówienie dla klientów przed
        25 rokiem życia dostają rabat 3%. Uwaga rabaty nie sumuję się, tylko wybierany
        jest korzystniejszy wariant. Uwzględniając te informacje wyznacz całkowitą
        cenę wszystkich zamówień.

        #todo czy ta funkcja jest ok?
        """
        client_and_final_price = self.client_and_price()
        print(client_and_final_price)
        today = date.today()

        for i, order in enumerate(self.orders):
            if order.customer.age < 25:
                client_and_final_price[f"{order.customer.name} {order.customer.surname}"] *= Decimal('0.97')

            elif (today - order.order_date).total_seconds() < 172_800:
                client_and_final_price[f"{order.customer.name} {order.customer.surname}"] *= Decimal('0.98')

        # {'JOHN MAYER': Decimal('5300'), 'ANNA SNOW': Decimal('7200')}
        # {'JOHN MAYER': Decimal('4986.7700'), 'ANNA SNOW': Decimal('6914.8800')}

        return client_and_final_price

    def get_clients_with_products_quantity_at_least(self, value: int) -> dict[str, int]:
        """
        Wyznacz liczbę klientów, którzy za każdym razem zamówili co najmniej x sztuk
        zamawianego produktu. Wartość zmiennej x przekazywana jest przykładowo jako
        argument metody. Informacje o takich klientach zapisz do pliku JSON.
        """
        client_and_quantity = {f"{o.customer.name} {o.customer.surname}": o.quantity for o in self.orders if
                               o.quantity >= value}
        save_to_json('order_app/data/client_and_quantity.json', client_and_quantity)
        return client_and_quantity

    def get_most_common_product_category(self):
        """
        Wyznacz kategorię, której produkty kupowano najczęściej.
        """
        grouped_by_category = {}
        grouped_by_frequency = defaultdict(list)

        for c in Category:
            grouped_by_category[c] = [o.product for o in self.orders if c == o.product.category]

        for category, products in grouped_by_category.items():
            grouped_by_frequency[len(products)].append(category)

        return max(grouped_by_frequency.items(), key=lambda pair: pair[0])[1]

    def get_monthly_statistics(self) -> list[tuple[str, int]]:
        """
        Wykonaj zestawienie, w którym podasz nazwę miesiąca oraz ilość
        produktów zamówionych w tym miesiącu. Zestawienie posortuj malejąco
        według ilości zamówionych produktów.
        """
        grouped_by_month = defaultdict(list)

        for order in self.orders:
            grouped_by_month[order.order_date.strftime('%B')].append(order.product.name)

        return sorted([(k, len(v)) for k, v in grouped_by_month.items()], key=lambda pair: pair[1], reverse=True)

    def get_monthly_statistics_with_category(self):
        """
        Wykonaj zestawienie, w którym podasz nazwę miesiąca oraz kategorię
        produktu, której produkty najchętniej w tym miesiącu zamawiano.

        #todo do poprawy? docelowo taki wynik
        # {'June': {<Category.A: 1>: ['LAPTOP', 'TV'], <Category.C: 3>: ['LAPTOP', 'TV']}}
        """
        grouped_by_month = defaultdict(dict)

        for order in self.orders:
            grouped_by_month[order.order_date.strftime('%B')][order.product.category] = \
                [grouped_by_month[order.order_date.strftime('%B')][order.product.category], order.product.name] \
                    if order.product.category in grouped_by_month[order.order_date.strftime('%B')] \
                    else order.product.name

        return dict(grouped_by_month)
