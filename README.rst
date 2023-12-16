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

.. Internal references

.. _fake.py: https://github.com/barseghyanartur/fake.py/
.. _Read the Docs: http://fakepy.readthedocs.io/
.. _Quick start: https://fakepy.readthedocs.io/en/latest/quick_start.html
.. _Recipes: https://fakepy.readthedocs.io/en/latest/recipes.html
.. _Factories: https://fakepy.readthedocs.io/en/latest/factories.html
.. _Customization: https://fakepy.readthedocs.io/en/latest/customization.html
.. _Creating PDF: https://fakepy.readthedocs.io/en/latest/creating_pdf.html
.. _Creating DOCX: https://fakepy.readthedocs.io/en/latest/creating_docx.html
.. _Creating images: https://fakepy.readthedocs.io/en/latest/creating_images.html
.. _Contributor guidelines: https://fakepy.readthedocs.io/en/latest/contributor_guidelines.html

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
types (such as `uuid`, `str`, `int`, `float`, `bool`) and byte content
for multiple file formats including `PDF`, `DOCX`, `PNG`, `SVG`, `BMP`,
and `GIF`.

The package also supports file creation on the filesystem and includes
factories (dynamic fixtures) compatible with `Django`_, `TortoiseORM`_,
`Pydantic`_ and `SQLAlchemy`_.

Features
========
- Generation of random texts, (person) names, emails, URLs, dates, IPs, and
  primitive Python data types.
- Support for various file formats (`PDF`, `DOCX`, `TXT`, `PNG`, `SVG`,
  `BMP`, `GIF`) and file creation on the filesystem.
- Basic factories for integration with `Django`_, `Pydantic`_,
  `TortoiseORM`_ and `SQLAlchemy`_.

Prerequisites
=============
Python 3.8+

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
- For tips on images creation see `Creating images`_.
- For guidelines on contributing check the `Contributor guidelines`_.

Usage
=====
Generate data
-------------
Person names
~~~~~~~~~~~~
.. code-block:: python

    from fake import FAKER

    FAKER.first_name()
    FAKER.last_name()
    FAKER.name()
    FAKER.username()

Random texts
~~~~~~~~~~~~
.. code-block:: python

    from fake import FAKER

    FAKER.slug()
    FAKER.word()
    FAKER.sentence()
    FAKER.paragraph()
    FAKER.text()

Internet
~~~~~~~~
.. code-block:: python

    from fake import FAKER

    FAKER.email()
    FAKER.url()
    FAKER.ipv4()

Filenames
~~~~~~~~~
.. code-block:: python

    from fake import FAKER

    FAKER.filename()

Primitive data types
~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    from fake import FAKER

    FAKER.pyint()
    FAKER.pybool()
    FAKER.pystr()
    FAKER.pyfloat()

Dates
~~~~~
.. code-block:: python

    from fake import FAKER

    FAKER.date()
    FAKER.date_time()

Generate files
--------------
As bytes
~~~~~~~~
.. code-block:: python

    from fake import FAKER

    FAKER.pdf()
    FAKER.docx()
    FAKER.png()
    FAKER.svg()
    FAKER.bmp()
    FAKER.gif()

As files on the file system
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    from fake import FAKER

    FAKER.pdf_file()
    FAKER.docx_file()
    FAKER.png_file()
    FAKER.svg_file()
    FAKER.bmp_file()
    FAKER.gif_file()
    FAKER.txt_file()

Factories
---------
This is how you could define a factory for `Django`_'s built-in ``User`` model.

.. code-block:: python

    from django.contrib.auth.models import User
    from fake import (
        FACTORY,
        DjangoModelFactory,
        pre_save,
        trait,
    )

    class UserFactory(DjangoModelFactory):

        username = FACTORY.username()
        first_name = FACTORY.first_name()
        last_name = FACTORY.last_name()
        email = FACTORY.email()
        last_login = FACTORY.date_time()
        is_superuser = False
        is_staff = False
        is_active = FACTORY.pybool()
        date_joined = FACTORY.date_time()

        class Meta:
            model = User
            get_or_create = ("username",)

        @trait
        def is_admin_user(self, instance: User) -> None:
            instance.is_superuser = True
            instance.is_staff = True
            instance.is_active = True

        @pre_save
        def _set_password(self, instance: User) -> None:
            instance.set_password("test")

And this is how you could use it:

.. code-block:: python

    # Create just one user
    user = UserFactory()

    # Create 5 users
    users = UserFactory.create_batch(5)

    # Create a user using `is_admin_user` trait
    user = UserFactory(is_admin_user=True)

Customize
---------
Make your own custom providers and utilize factories with them.

.. code-block:: python

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

    FAKER.postal_code()

    from fake import ModelFactory


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

The file generation part of `fake.py`_ are modelled after the `faker-file`_.
You don't get a large variety of file types supported and you don't have that
much control over the content of the files generated, but you get
dependency-free valid files and if that's all you need, you don't need to look
further.

However, at any point, if you discover that you "need more", go for `Faker`_,
`factory_boy`_ and `faker-file`_ combination.

License
=======

MIT

Author
======

Artur Barseghyan <artur.barseghyan@gmail.com>
