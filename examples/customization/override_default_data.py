from fake import Factory, Faker

from data import FIRST_NAMES, LAST_NAMES, WORDS

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "FACTORY",
    "FAKER",
)


class FakerOverrideDefaultData(Faker):
    """Faker class for custom names and words."""

    def load_names(self) -> None:
        """Override default first- and last-names dictionaries."""
        self._first_names = FIRST_NAMES
        self._last_names = LAST_NAMES

    def load_words(self) -> None:
        """Override default words dictionary."""
        self._words = WORDS


FAKER = FakerOverrideDefaultData(alias="override_default_data")
FACTORY = Factory(FAKER)
