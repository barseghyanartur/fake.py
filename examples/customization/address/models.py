from dataclasses import dataclass
from datetime import date

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "Address",
    "Person",
)


@dataclass
class Address:
    id: int
    address_line: str
    postal_code: str
    city: str
    region: str

    def __str__(self) -> str:
        return self.address_line


@dataclass
class Person:
    id: int
    first_name: str
    last_name: str
    email: str
    dob: date
    address: Address

    def __str__(self) -> str:
        return self.username
