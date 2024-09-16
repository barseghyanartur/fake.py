=======
fake.py
=======
.. External references

.. _Faker: https://faker.readthedocs.io/
.. _factory_boy: https://factoryboy.readthedocs.io/
.. _faker-file: https://faker-file.readthedocs.io/
.. _Pillow: https://python-pillow.org/
.. _dateutil: https://dateutil.readthedocs.io/
.. _Django: https://www.djangoproject.com/
.. _TortoiseORM: https://tortoise.github.io/
.. _Pydantic: https://docs.pydantic.dev/
.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _SQLModel: https://sqlmodel.tiangolo.com/
.. _Pathy: https://github.com/justindujardin/pathy
.. _django-storages: https://django-storages.readthedocs.io

.. Internal references

.. _fake.py: https://github.com/barseghyanartur/fake.py/
.. _Read the Docs: http://fakepy.readthedocs.io/
.. _Quick start: https://fakepy.readthedocs.io/en/latest/quick_start.html
.. _Recipes: https://fakepy.readthedocs.io/en/latest/recipes.html
.. _Factories: https://fakepy.readthedocs.io/en/latest/factories.html
.. _Customization: https://fakepy.readthedocs.io/en/latest/customization.html
.. _Creating PDF: https://fakepy.readthedocs.io/en/latest/creating_pdf.html
.. _Creating DOCX: https://fakepy.readthedocs.io/en/latest/creating_docx.html
.. _Creating ODT: https://fakepy.readthedocs.io/en/latest/creating_odt.html
.. _Creating images: https://fakepy.readthedocs.io/en/latest/creating_images.html
.. _Examples: https://github.com/barseghyanartur/fake.py/tree/main/examples
.. _CLI: https://fakepy.readthedocs.io/en/latest/cli.html
.. _Contributor guidelines: https://fakepy.readthedocs.io/en/latest/contributor_guidelines.html

.. Related projects

.. _fake-py-pathy-storage: https://github.com/barseghyanartur/fake-py-pathy-storage
.. _fake-py-django-storage: https://github.com/barseghyanartur/fake-py-django-storage
.. _fake-py-qt: https://github.com/barseghyanartur/fake-py-qt
.. _fake-py-wasm: https://github.com/barseghyanartur/fake-py-wasm

Minimalistic, standalone alternative fake data generator with no dependencies.

.. image:: https://img.shields.io/pypi/v/fake.py.svg
   :target: https://pypi.python.org/pypi/fake.py
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/fake.py.svg
    :target: https://pypi.python.org/pypi/fake.py/
    :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/fake.py/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/barseghyanartur/fake.py/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/fakepy/badge/?version=latest
    :target: http://fakepy.readthedocs.io
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/fake.py/#License
   :alt: MIT

.. image:: https://coveralls.io/repos/github/barseghyanartur/fake.py/badge.svg?branch=main&service=github
    :target: https://coveralls.io/github/barseghyanartur/fake.py?branch=main
    :alt: Coverage

`fake.py`_ is a standalone, portable library designed for generating various
random data types for testing.

It offers a simplified, dependency-free alternative for creating random
texts, (person) names, URLs, dates, file names, IPs, primitive Python data
types (such as `uuid`, `str`, `int`, `float`, `bool`), GEO data such as city,
country, geo-location, country code, latitude, longitude and locales,
IBANs and ISBNs, as well as byte content for multiple file formats
including `PDF`, `DOCX`, `ODT`, `PNG`, `SVG`, `BMP`, `GIF`, `TIF`, `PPM`,
`WAV`, `ZIP`, `TAR` and `EML`.

The package also supports file creation on the filesystem and includes
factories (dynamic fixtures) compatible with `Django`_, `TortoiseORM`_,
`Pydantic`_ and `SQLAlchemy`_ (which means it works with `SQLModel`_ too).

Features
========
- Generation of random texts, (person) names, emails, URLs, dates, IPs, and
  primitive Python data types.
- Support for various file formats (`PDF`, `DOCX`, `ODT`, `TXT`, `PNG`, `SVG`,
  `BMP`, `GIF`, `TIF`, `PPM`, `WAV`, `ZIP`, `TAR`, `EML`) and file creation
  on the filesystem.
- Basic factories for integration with `Django`_, `Pydantic`_,
  `TortoiseORM`_ and `SQLAlchemy`_.
- `CLI`_ for generating data from command line.

Prerequisites
=============
Python 3.9+

Installation
============
pip
---

.. code-block:: sh

    pip install fake.py

Download and copy
-----------------
``fake.py`` is the sole, self-contained module of the package. It includes
tests too. If it's more convenient to you, you could simply download the
``fake.py`` module and include it in your repository.

Since tests are included, it won't have a negative impact on your test
coverage (you might need to apply tweaks to your coverage configuration).

Documentation
=============
- Documentation is available on `Read the Docs`_.
- For various ready to use code examples see the `Recipes`_.
- For tips on how to use the factories see the `Factories`_.
- For customization tips see the `Customization`_.
- For tips on ``PDF`` creation see `Creating PDF`_.
- For tips on ``DOCX`` creation see `Creating DOCX`_.
- For tips on ``ODT`` creation see `Creating ODT`_.
- For tips on images creation see `Creating images`_.
- For various implementation examples, see the `Examples`_.
- For CLI documentation, see the `CLI`_.
- For guidelines on contributing check the `Contributor guidelines`_.

Usage
=====
Generate data
-------------
Person names
~~~~~~~~~~~~
.. code-block:: python
    :name: test_person_names

    from fake import FAKER

    FAKER.first_name()  # str
    FAKER.first_names()  # list[str]
    FAKER.last_name()  # str
    FAKER.last_names()  # list[str]
    FAKER.name()  # str
    FAKER.names()  # list[str]
    FAKER.username()  # str
    FAKER.usernames()  # list[str]

Random texts
~~~~~~~~~~~~
.. code-block:: python
    :name: test_random_texts

    from fake import FAKER

    FAKER.paragraph()  # str
    FAKER.paragraphs()  # list[str]
    FAKER.sentence()  # str
    FAKER.sentences()  # list[str]
    FAKER.slug()  # str
    FAKER.slugs()  # list[str]
    FAKER.text()  # str
    FAKER.texts()  # list[str]
    FAKER.word()  # str
    FAKER.words()  # list[str]

Internet
~~~~~~~~
.. code-block:: python
    :name: test_internet

    from fake import FAKER

    FAKER.company_email()  # str
    FAKER.domain_name()  # str
    FAKER.email()  # str
    FAKER.free_email()  # str
    FAKER.free_email_domain()  # str
    FAKER.image_url()  # str
    FAKER.ipv4()  # str
    FAKER.tld()  # str
    FAKER.url()  # str

Filenames
~~~~~~~~~
.. code-block:: python
    :name: test_filenames

    from fake import FAKER

    FAKER.file_extension()  # str
    FAKER.file_name()  # str
    FAKER.mime_type()  # str

Primitive data types
~~~~~~~~~~~~~~~~~~~~
.. code-block:: python
    :name: test_primitive_data_types

    from fake import FAKER

    FAKER.pybool()  # bool
    FAKER.pyfloat()  # flot
    FAKER.pyint()  # int
    FAKER.pystr()  # str
    FAKER.uuid()  # uuid.UUID

Dates
~~~~~
.. code-block:: python
    :name: test_dates

    from fake import FAKER

    FAKER.date()  # datetime.date
    FAKER.date_time()  # datetime.datetime

Geographic data
~~~~~~~~~~~~~~~
.. code-block:: python
    :name: test_geographic_data

    from fake import FAKER

    FAKER.city()  # str
    FAKER.country()  # str
    FAKER.geo_location()  # str
    FAKER.country_code()  # str
    FAKER.locale()  # str
    FAKER.latitude()  # float
    FAKER.longitude()  # float
    FAKER.latitude_longitude()  # tuple[float, float]

Books
~~~~~
.. code-block:: python
    :name: test_books

    from fake import FAKER

    FAKER.isbn10()  # str
    FAKER.isbn13()  # str

Banking
~~~~~~~
.. code-block:: python
    :name: test_banking

    from fake import FAKER

    FAKER.iban()  # str

Generate files
--------------
As bytes
~~~~~~~~
.. code-block:: python
    :name: test_generate_files_as_bytes

    from fake import FAKER

    FAKER.bmp()  # bytes
    FAKER.docx()  # bytes
    FAKER.gif()  # bytes
    FAKER.odt()  # bytes
    FAKER.pdf()  # bytes
    FAKER.png()  # bytes
    FAKER.ppm()  # bytes
    FAKER.svg()  # bytes
    FAKER.tif()  # bytes
    FAKER.wav()  # bytes

As files on the file system
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python
    :name: test_generate_files_as_files_on_file_system

    from fake import FAKER

    FAKER.bmp_file()  # str
    FAKER.docx_file()  # str
    FAKER.gif_file()  # str
    FAKER.odt_file()  # str
    FAKER.pdf_file()  # str
    FAKER.png_file()  # str
    FAKER.ppm_file()  # str
    FAKER.svg_file()  # str
    FAKER.tif_file()  # str
    FAKER.wav_file()  # str
    FAKER.txt_file()  # str

Factories/dynamic fixtures
--------------------------
This is how you could define factories for `Django`_'s built-in ``Group``
and ``User`` models.

*Filename: factories.py*

.. code-block:: python
    :name: test_factories

    from django.contrib.auth.models import Group, User
    from fake import (
        DjangoModelFactory,
        FACTORY,
        PostSave,
        PreSave,
        trait,
    )


    class GroupFactory(DjangoModelFactory):
        """Group factory."""

        name = FACTORY.word()

        class Meta:
            model = Group
            get_or_create = ("name",)


    def set_password(user: User, password: str) -> None:
        """Helper function for setting password for the User."""
        user.set_password(password)


    def add_to_group(user: User, name: str) -> None:
        """Helper function for adding the User to a Group."""
        group = GroupFactory(name=name)
        user.groups.add(group)


    class UserFactory(DjangoModelFactory):
        """User factory."""

        username = FACTORY.username()
        first_name = FACTORY.first_name()
        last_name = FACTORY.last_name()
        email = FACTORY.email()
        date_joined = FACTORY.date_time()
        last_login = FACTORY.date_time()
        is_superuser = False
        is_staff = False
        is_active = FACTORY.pybool()
        password = PreSave(set_password, password="test1234")
        group = PostSave(add_to_group, name="Test group")

        class Meta:
            model = User
            get_or_create = ("username",)

        @trait
        def is_admin_user(self, instance: User) -> None:
            """Trait."""
            instance.is_superuser = True
            instance.is_staff = True
            instance.is_active = True

And this is how you could use it:

.. code-block:: python

    # Create just one user
    user = UserFactory()

    # Create 5 users
    users = UserFactory.create_batch(5)

    # Create a user using `is_admin_user` trait
    user = UserFactory(is_admin_user=True)

    # Create a user with custom password
    user = UserFactory(
        password=PreSave(set_password, password="another-password"),
    )

    # Add a user to another group
    user = UserFactory(
        group=PostSave(add_to_group, name="Another group"),
    )

    # Or even add user to multiple groups at once
    user = UserFactory(
        group_1=PostSave(add_to_group, name="Another group"),
        group_2=PostSave(add_to_group, name="Yet another group"),
    )

Customize
---------
Make your own custom providers and utilize factories with them.

*Filename: custom_fake.py*

.. code-block:: python
    :name: test_customize

    import random
    import string

    from fake import Faker, Factory, provider


    class CustomFaker(Faker):

        @provider
        def postal_code(self) -> str:
            number_part = "".join(random.choices(string.digits, k=4))
            letter_part = "".join(random.choices(string.ascii_uppercase, k=2))
            return f"{number_part} {letter_part}"


    FAKER = CustomFaker()
    FACTORY = Factory(FAKER)

Now you can use it as follows (make sure to import your custom instances
of ``FAKER`` and ``FACTORY``):

.. code-block:: python

    from custom_fake import FAKER  # Custom `FAKER` instance

    FAKER.postal_code()

Or as follows:

.. code-block:: python

    from fake import ModelFactory

    from custom_fake import FACTORY  # Custom `FACTORY` instance


    class AddressFactory(ModelFactory):

        # ... other definitions
        postal_code = FACTORY.postal_code()
        # ... other definitions

        class Meta:
            model = Address

Tests
=====

Run the tests with unittest:

.. code-block:: sh

    python -m unittest fake.py

Or pytest:

.. code-block:: sh

    pytest

Differences with alternatives
=============================
`fake.py`_ is `Faker`_ + `factory_boy`_ + `faker-file`_ in one package,
radically simplified and reduced in features, but without any external
dependencies (not even `Pillow`_ or `dateutil`_).

`fake.py`_ is modeled after the famous `Faker`_ package. Its' API is highly
compatible, although drastically reduced. It's not multilingual and does not
support postal codes or that many RAW file formats. However, you could easily
include it in your production setup without worrying about yet another
dependency.

On the other hand, `fake.py`_ factories look quite similar to `factory_boy`_
factories, although again - drastically simplified and reduced in
features.

The file generation part of `fake.py`_ is modelled after the `faker-file`_.
You don't get a large variety of file types supported and you don't have that
much control over the content of the files generated, but you get
dependency-free valid files and if that's all you need, you don't need to look
further.

However, at any point, if you discover that you "need more", go for `Faker`_,
`factory_boy`_ and `faker-file`_ combination.

Related projects
================
- `fake-py-pathy-storage`_: `Pathy`_ backed cloud storages for `fake.py`_.
  Supports `AWS S3`, `Google Cloud Storage` and `Azure Cloud Storage`.
- `fake-py-django-storage`_: `Django`_ and `django-storages`_ backed storages
  for `fake.py`_. Among others, supports `AWS S3`, `Google Cloud Storage` and
  `Azure Cloud Storage`.
- `fake-py-qt`_: Graphical user interface to `fake.py`_.
- `fake-py-wasm`_: `fake.py`_ on WASM (web assembly).

Writing documentation
=====================

Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======

MIT

Support
=======
For security issues contact me at the e-mail given in the `Author`_ section.

For overall issues, go to `GitHub <https://github.com/barseghyanartur/fake.py/issues>`_.

Author
======

Artur Barseghyan <artur.barseghyan@gmail.com>
