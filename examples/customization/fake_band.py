import random

from fake import Factory, Faker, provider

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "FACTORY",
    "FAKER",
)

BANDS = [
    "Aerosmith",
    "Agata Kristi",
    "Anathema",
    "Bjork",
    "Black Sabbath",
    "Blonde Redhead",
    "Cocteau Twins",
    "Comus",
    "Dead Can Dance",
    "Depeche Mode",
    "Focus",
    "Kalinov Most",
    "Kate Bush",
    "King Crimson",
    "Kolibri",
    "Lais",
    "Led Zeppelin",
    "Linda",
    "Nirvana",
    "Nor Dar",
    "Oasis",
    "Opeth",
    "Pink Floyd",
    "Portishead",
    "Radiohead",
    "Red Hot Chili Peppers",
    "Sinead O'Connor",
    "Siouxsie and the Banshees",
    "System of a Down",
    "The Beatles",
    "The Cranberries",
    "The Cure",
    "The Rolling Stones",
    "The Velvet Underground",
    "Tiamat",
    "Van der Graaf Generator",
    "Yes",
]


class FakerBand(Faker):
    """Custom Faker class for bands."""

    @provider
    def band_name(self) -> str:
        return random.choice(BANDS)


FAKER = FakerBand(alias="band")
FACTORY = Factory(FAKER)
