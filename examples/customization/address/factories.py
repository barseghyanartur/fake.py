from fake import ModelFactory, SubFactory, post_save, pre_save
from override_default_data import FACTORY as OVERRIDE_DEFAULT_DATA_FACTORY

from address.models import Address, Person
from fake_address import FACTORY as ADDRESS_FACTORY

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "AddressFactory",
    "PersonFactory",
)


class AddressFactory(ModelFactory):
    id = ADDRESS_FACTORY.pyint()
    address_line = ADDRESS_FACTORY.address_line()
    postal_code = ADDRESS_FACTORY.postal_code()
    city = ADDRESS_FACTORY.city()
    region = ADDRESS_FACTORY.region()

    class Meta:
        model = Address

    @pre_save
    def _pre_save_method(self, instance):
        instance._pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        instance._post_save_called = True


class PersonFactory(ModelFactory):
    id = OVERRIDE_DEFAULT_DATA_FACTORY.pyint()
    first_name = OVERRIDE_DEFAULT_DATA_FACTORY.first_name()
    last_name = OVERRIDE_DEFAULT_DATA_FACTORY.last_name()
    email = OVERRIDE_DEFAULT_DATA_FACTORY.email()
    dob = OVERRIDE_DEFAULT_DATA_FACTORY.date()
    address = SubFactory(AddressFactory)

    class Meta:
        model = Person

    @pre_save
    def _pre_save_method(self, instance):
        instance._pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        instance._post_save_called = True
