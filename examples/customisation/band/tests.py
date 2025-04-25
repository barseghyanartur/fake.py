import unittest

from fake import FILE_REGISTRY

from band.factories import BandFactory
from band.models import Band

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2025 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("BandFakerTestCase",)


class BandFakerTestCase(unittest.TestCase):
    def tearDown(self):
        FILE_REGISTRY.clean_up()

    def test_sub_factory(self) -> None:
        band = BandFactory()

        # Testing Factory
        self.assertIsInstance(band.id, int)
        self.assertIsInstance(band.name, str)

        # Testing batch creation
        bands = BandFactory.create_batch(5)
        self.assertEqual(len(bands), 5)
        self.assertIsInstance(bands[0], Band)
