import random
import string

from fake import Factory, Faker, provider

from data import CITIES, REGIONS, STREET_NAMES

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "FACTORY",
    "FAKER",
)


class FakerAddress(Faker):
    """Custom Faker class for addresses."""

    @provider
    def address_line(self) -> str:
        """Generate a random Dutch address line like 'Oranjestraat 1'.

        :return: A randomly generated Dutch address line as a string.
        :rtype: str
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
        :rtype: str
        """
        number_part = "".join(random.choices(string.digits, k=4))
        letter_part = "".join(random.choices(string.ascii_uppercase, k=2))
        return f"{number_part} {letter_part}"


FAKER = FakerAddress(alias="address")
FACTORY = Factory(FAKER)
