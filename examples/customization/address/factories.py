from fake import ModelFactory, SubFactory, post_save, pre_save

from address.models import Address, Person
from custom_fake import FACTORY

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "AddressFactory",
    "PersonFactory",
)


class AddressFactory(ModelFactory):
    id = FACTORY.pyint()
    address_line = FACTORY.address_line()
    postal_code = FACTORY.postal_code()
    city = FACTORY.city()
    region = FACTORY.region()

    class Meta:
        model = Address

    @pre_save
    def _pre_save_method(self, instance):
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        instance.post_save_called = True


class PersonFactory(ModelFactory):
    id = FACTORY.pyint()
    first_name = FACTORY.first_name()
    last_name = FACTORY.last_name()
    email = FACTORY.email()
    dob = FACTORY.date()
    address = SubFactory(AddressFactory)

    class Meta:
        model = Person

    @pre_save
    def _pre_save_method(self, instance):
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        instance.post_save_called = True
