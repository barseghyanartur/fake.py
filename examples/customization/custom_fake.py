import random
import string

from fake import Factory, Faker, provider

from data import CITIES, FIRST_NAMES, LAST_NAMES, REGIONS, STREET_NAMES, WORDS

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "FACTORY",
    "FAKER",
)


class CustomFaker(Faker):
    """Custom Faker class."""

    def load_names(self) -> None:
        """Override default first- and last-names dictionaries."""
        self._first_names = FIRST_NAMES
        self._last_names = LAST_NAMES

    def load_words(self) -> None:
        """Override default words dictionary."""
        self._words = WORDS

    @provider
    def address_line(self) -> str:
        """Generate a random Dutch address line like 'Oranjestraat 1'.

        :return: A randomly generated Dutch address line as a string.
        """
        # Generate components of the address
        street = random.choice(STREET_NAMES)
        house_number = random.randint(1, 200)
        suffixes = [""] * 10 + ["A", "B", "C"]  # Optional suffixes
        suffix = random.choice(suffixes)

        # Combine components into a Dutch address format
        return f"{street} {house_number}{suffix}"

    @provider
    def city(self) -> str:
        return random.choice(CITIES)

    @provider
    def region(self) -> str:
        return random.choice(REGIONS)

    @provider
    def postal_code(self) -> str:
        """Generate a random Dutch postal code in the format '1234 AB'.

        :return: A randomly generated Dutch postal code as a string.
        """
        number_part = "".join(random.choices(string.digits, k=4))
        letter_part = "".join(random.choices(string.ascii_uppercase, k=2))
        return f"{number_part} {letter_part}"


FAKER = CustomFaker()
FACTORY = Factory(FAKER)
