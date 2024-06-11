import unittest

from fake import FILE_REGISTRY

from address.factories import AddressFactory, PersonFactory
from address.models import Address, Person
from data import CITIES, REGIONS

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("AddressFakerTestCase",)


class AddressFakerTestCase(unittest.TestCase):
    def tearDown(self):
        FILE_REGISTRY.clean_up()

    def test_sub_factory(self) -> None:
        person = PersonFactory()

        # Testing SubFactory
        self.assertIsInstance(person.address, Address)
        self.assertIsInstance(person.address.id, int)

        # Testing Factory
        self.assertIsInstance(person.id, int)

        # Testing hooks
        self.assertTrue(
            hasattr(person, "_pre_save_called") and person._pre_save_called
        )
        self.assertTrue(
            hasattr(person, "_post_save_called") and person._post_save_called
        )
        self.assertTrue(
            hasattr(person.address, "_pre_save_called")
            and person.address._pre_save_called
        )
        self.assertTrue(
            hasattr(person.address, "_post_save_called")
            and person.address._post_save_called
        )

        # Testing batch creation
        persons = PersonFactory.create_batch(5)
        self.assertEqual(len(persons), 5)
        self.assertIsInstance(persons[0], Person)

        # Testing custom addresses
        address = AddressFactory()
        self.assertIn(address.city, CITIES)
        self.assertIn(address.region, REGIONS)
