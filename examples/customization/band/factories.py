from band.models import Band
from fake import ModelFactory

from fake_band import FACTORY

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("BandFactory",)


class BandFactory(ModelFactory):
    id = FACTORY.pyint()
    name = FACTORY.band_name()

    class Meta:
        model = Band
        get_or_create = ("name",)
