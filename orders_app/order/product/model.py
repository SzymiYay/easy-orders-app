from dataclasses import dataclass
from enum import Enum, auto
from decimal import Decimal


class Category(Enum):
    A = auto()
    B = auto()
    C = auto()


@dataclass
class Product:
    name: str
    price: Decimal
    category: Category
