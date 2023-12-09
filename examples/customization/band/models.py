from dataclasses import dataclass

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("Band",)


@dataclass
class Band:
    id: int
    name: str

    def __str__(self) -> str:
        return self.address_line
