=======
fake.py
=======
.. External references

.. _Faker: https://faker.readthedocs.io/

Minimalistic, standalone alternative fake data generator with no dependencies.

.. contents:: Table of Contents
   :depth: 2

Overview
========

``fake.py`` is a standalone and portable library that allows you to generate
various types of random data for testing and other purposes. The package
provides a simplified, dependency-free alternative for generating random
words, sentences, paragraphs, file names, URLs, PDFs, images, person names
and more.

Requirements
============

* Python 3.8+

Installation
============
pip
---

.. code-block:: bash

    pip install fake.py

Download and copy
-----------------
``fake.py`` is the sole, self-contained module of the package. It includes
tests too. If it's more convenient to you, you could simply download the
``fake.py`` module and include it in your repository.

Since tests are included, it won't have a negative impact on your test
coverage (you might need to apply tweaks to your coverage configuration).

Usage
=====
**Imports and initialization**

.. code-block:: python

    from fake import Faker

    FAKER = Faker()

**first_name**

Returns a random first name.

.. code-block:: python

    FAKER.first_name()

**last_name**

Returns a random last name.

.. code-block:: python

    FAKER.last_name()

**name**

Returns a random full name.

.. code-block:: python

    FAKER.name()

**word**

Returns a random word from the Zen of Python.

.. code-block:: python

    FAKER.word()

**words**

Returns a list of ``nb`` random words from the Zen of Python.

.. code-block:: python

    FAKER.words()

Arguments:

- ``nb`` (type: ``int``, default value: ``5``) is an optional argument.

**sentence**

Returns a random sentence with ``nb_words`` number of words.

.. code-block:: python

    FAKER.sentence()

Arguments:

- ``nb_words`` (type: ``int``, default value: ``5``) is an optional argument.

**sentences**

Returns ``nb`` number of random sentences.

.. code-block:: python

    FAKER.sentences()

Arguments:

- ``nb`` (type: ``int``, default value: ``3``) is an optional argument.

**paragraph**

Returns a random paragraph with ``nb_sentences`` number of sentences.

.. code-block:: python

    FAKER.paragraph()

Arguments:

- ``nb_sentences`` (type: ``int``, default value: ``5``) is an optional
  argument.

**paragraphs**

Returns ``nb`` number of random paragraphs.

.. code-block:: python

    FAKER.paragraphs()

Arguments:

- ``nb`` (type: ``int``, default value: ``3``) is an optional argument.

**text**

Returns random text with up to ``nb_chars`` characters.

.. code-block:: python

    FAKER.text()

Arguments:

- ``nb_chars`` (type: ``int``, default value: ``200``) is an optional argument.

**file_name**

Returns a random file name with the given extension.

.. code-block:: python

    FAKER.file_name()

Arguments:

- ``extension`` (type: ``str``, default value: ``txt``) is an optional
  argument.

**email**

Returns a random email with the specified domain.

.. code-block:: python

    FAKER.email()

Arguments:

- ``domain`` (type: ``str``, default value: ``example.com``) is an optional
  argument.

**url**

Returns a random URL.

.. code-block:: python

    FAKER.url()

Arguments:

- ``protocols`` (type: ``Optional[Tuple[str]]``, default value: ``None``) is
  an optional argument.
- ``tlds`` (type: ``Optional[Tuple[str]]``, default value: ``None``) is
  an optional argument.
- ``suffixes`` (type: ``Optional[Tuple[str]]``, default value: ``None``) is
  an optional argument.

**pyint**

Returns a random integer between ``min_value`` and ``max_value``.

.. code-block:: python

    FAKER.pyint()

Arguments:

- ``min_value`` (type: ``int``, default value: ``0``) is an optional argument.
- ``max_value`` (type: ``int``, default value: ``9999``) is an optional
  argument.

**pybool**

Returns a random boolean value.

.. code-block:: python

    FAKER.pybool()

**pystr**

Returns a random string of ``nb_chars`` length.

.. code-block:: python

    FAKER.pystr()

Arguments:

- ``nb_chars`` (type: ``int``, default value: ``20``) is an optional argument.

**pyfloat**

Returns a random float between ``min_value`` and ``max_value``.

.. code-block:: python

    FAKER.pyfloat()

Arguments:

- ``min_value`` (type: ``float``, default value: ``0.0``) is an optional
  argument.
- ``max_value`` (type: ``float``, default value: ``10.00``) is an optional
  argument.

**ipv4**

Returns a random IPv4 address.

.. code-block:: python

    FAKER.ipv4()

**date_between**

Generates a random date between ``start_date`` and ``end_date``.

.. code-block:: python

    FAKER.date_between(start_date="-1d", end_date="+1d")

Arguments:

- ``start_date`` (type: ``str``) is a required argument.
- ``end_date`` (type: ``str``, default value: ``+0d``) is an optional
  argument.

**date_time_between**

Generates a random datetime between ``start_date`` and ``end_date``.

.. code-block:: python

    FAKER.date_time_between(start_date="-1d", end_date="+1d")

Arguments:

- ``start_date`` (type: ``str``) is a required argument.
- ``end_date`` (type: ``str``, default value: ``+0d``) is an optional
  argument.

**pdf**

Generates a content (``bytes``) of a PDF document.

.. code-block:: python

    FAKER.pdf()

Arguments:

- ``nb_pages`` (type: ``int``, default value: ``1``) is an optional argument.
- ``generator``
  (type: ``Union[Type[TextPdfGenerator], Type[GraphicPdfGenerator]]``,
  default value: ``GraphicPdfGenerator``) is an optional argument.

**image**

Generates a content (``bytes``) of a image of the specified format and colour.

.. code-block:: python

    FAKER.image()  # Supported formats are `png`, `svg`, `bmp` and `gif`

Arguments:

- ``image_format`` (type: ``str``, default value: ``png``) is an optional
  argument.
- ``size`` (type: ``Tuple[int, int]``, default value: ``(100, 100)``) is an
  optional argument.
- ``color`` (type: ``Tuple[int, int, int]``, default value: ``(0, 0, 255)``)
  is an optional argument.

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
