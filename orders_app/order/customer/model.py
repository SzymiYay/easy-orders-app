from dataclasses import dataclass


@dataclass
class Customer:
    name: str
    surname: str
    age: int
    email: str