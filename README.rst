=======
fake.py
=======
.. External references

.. _Faker: https://faker.readthedocs.io/
.. _Django: https://www.djangoproject.com/
.. _TortoiseORM: https://tortoise.github.io/
.. _Pydantic: https://docs.pydantic.dev/

.. Internal references

.. _Read the Docs: http://fakepy.readthedocs.io/
.. _Quick start: https://fakepy.readthedocs.io/en/latest/quick_start.html
.. _Recipes: https://fakepy.readthedocs.io/en/latest/recipes.html
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

.. contents:: Table of Contents
   :depth: 2

Overview
========
``fake.py`` is a standalone, portable library designed for generating various
random data types for testing.

It offers a simplified, dependency-free alternative for creating random
texts, (person) names, URLs, dates, file names, IPs, primitive Python data
types (such as `uuid`, `str`, `int`, `float`, `bool`) and byte content
for multiple file formats including `PDF`, `DOCX`, `PNG`, `SVG`, `BMP`,
and `GIF`.

The package also supports file creation on the filesystem and includes
factories (dynamic fixtures) compatible with `Django`_, `TortoiseORM`_,
and `Pydantic`_.

Features
========
- Generation of random texts, (person) names, emails, URLs, dates, IPs, and
  primitive Python data types.
- Support for various file formats (`PDF`, `DOCX`, `TXT`, `PNG`, `SVG`,
  `BMP`, `GIF`) and file creation on the filesystem.
- Basic factories for integration with `Django`_, `Pydantic`_,
  and `TortoiseORM`_.

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

    from django.conf import settings
    from django.contrib.auth.models import User
    from fake import (
        FACTORY,
        DjangoModelFactory,
        FileSystemStorage,
        SubFactory,
        pre_save,
    )

    STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")

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

        @pre_save
        def __set_password(instance):
            instance.set_password("test")

And this is how you could use it:

.. code-block:: python

    user = UserFactory()
    users = UserFactory.create_batch(5)

Tests
=====

Run the tests with unittest:

.. code-block:: bash

    python -m unittest

Or pytest:

.. code-block:: bash

    pytest

Differences with `Faker`_
=========================
``fake.py`` is modeled after the famous `Faker`_ package. Its' API is highly
compatible, although drastically reduced. It's not multilingual and does not
support postal codes or that many RAW file formats. However, you could easily
include it in your production setup without worrying about yet another
dependency.

License
=======

MIT

Author
======

Artur Barseghyan <artur.barseghyan@gmail.com>
