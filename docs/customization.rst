Customization
=============
- The ``fake.FAKER`` is an instance of the ``fake.Faker`` class.
- The ``fake.FACTORY`` is an instance of the ``fake.Factory`` class,
  initialized with ``fake.FAKER`` instance.

The ``Faker`` class is easy to customize. See the following example:

*Filename: custom_fake.py*

.. code-block:: python
    :name: test_customization_custom_fake

    import random
    import string

    from fake import Faker, Factory, provider


    # Custom first names dictionary
    FIRST_NAMES = [
        "Anahit",
        "Ani",
        "Aram",
        "Areg",
        "Artur",
        "Astghik",
        "Atom",
        "Barsegh",
        "Gaiane",
        "Gor",
        "Hakob",
        "Hasmik",
        "Levon",
        "Lilit",
        "Mariam",
        "Nare",
        "Narek",
        "Nune",
        "Raffi",
        "Shant",
        "Tatev",
        "Tigran",
        "Vahan",
        "Vardan",
    ]

    # Custom last names dictionary
    LAST_NAMES = [
        "Amatouni",
        "Avagyan",
        "Danielyan",
        "Egoyan",
        "Gevorgyan",
        "Gnouni",
        "Grigoryan",
        "Hakobyan",
        "Harutyunyan",
        "Hovhannisyan",
        "Karapetyan",
        "Khachatryan",
        "Manukyan",
        "Melikyan",
        "Mkrtchyan",
        "Petrosyan",
        "Sahakyants",
        "Sargsyan",
        "Saroyan",
        "Sedrakyan",
        "Simonyan",
        "Stepanyan",
        "Ter-Martirosyan",
        "Vardanyan",
    ]

    # Custom words dictionary
    WORDS = [
        "time", "person", "year", "way", "day", "thing", "man", "world",
        "life", "hand", "part", "child", "eye", "woman", "place", "work",
        "week", "case", "point", "government", "company", "number", "group",
        "problem", "fact", "be", "have", "do", "say", "get", "make", "go",
        "know", "take", "see", "come", "think", "look", "want", "give",
        "use", "find", "tell", "ask", "work", "seem", "feel", "try", "leave",
        "call", "good", "new", "first", "last", "long", "great", "little",
        "own", "other", "old", "right", "big", "high", "different", "small",
        "large", "next", "early", "young", "important", "few", "public",
        "bad", "same", "able", "to", "of", "in", "for", "on", "with", "as",
        "at", "by", "from", "up", "about", "into", "over", "after",
        "beneath", "under", "above", "the", "and", "a", "that", "I", "it",
        "not",
    ]

    STREET_NAMES = [
        "Bosweg",
        "Groningerweg",
        "Jasmijnstraat",
        "Noordstraat",
        "Ooststraat",
        "Oranjestraat",
        "Prinsengracht",
        "Ringweg",
        "Weststraat",
        "Zonnelaan",
        "Zuidstraat",
    ]

    CITIES = [
        "Amsterdam",
        "Delft",
        "Den Haag",
        "Groningen",
        "Leiden",
        "Nijmegen",
    ]

    REGIONS = [
        "Friesland",
        "Groningen",
        "Limburg",
        "Utrecht",
    ]


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

The ``postal_code`` is the provider method and shall be decorated with
``@provider`` decorator.

You can now use both ``FAKER`` and ``FACTORY`` as you would normally do.

----

*Filename: models.py*

.. code-block:: python
    :name: test_customization_models

    from dataclasses import dataclass
    from datetime import date


    @dataclass
    class Address:
        id: int
        address_line: str
        postal_code: str
        city: str
        region: str

        def __str__(self) -> str:
            return self.address_line


    @dataclass
    class Person:
        id: int
        first_name: str
        last_name: str
        email: str
        dob: date
        address: Address

        def __str__(self) -> str:
            return self.username

----

*Filename: factories.py*

.. code-block:: python
    :name: test_customization_factories

    from fake import ModelFactory, SubFactory, post_save, pre_save

    from models import Address, Person
    from custom_fake import FACTORY


    class AddressFactory(ModelFactory):
        id = FACTORY.pyint()
        address_line = FACTORY.address_line()
        postal_code = FACTORY.postal_code()
        city = FACTORY.city()
        region = FACTORY.region()

        class Meta:
            model = Address


    class PersonFactory(ModelFactory):
        id = FACTORY.pyint()
        first_name = FACTORY.first_name()
        last_name = FACTORY.last_name()
        email = FACTORY.email()
        dob = FACTORY.date()
        address = SubFactory(AddressFactory)

        class Meta:
            model = Person
