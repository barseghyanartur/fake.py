========
faker.py
========
.. External references

.. _Faker: https://faker.readthedocs.io/

Minimalistic, standalone alternative fake data generator with no dependencies.

.. contents:: Table of Contents
   :depth: 2

Overview
========

``faker.py`` is a standalone and portable library that allows you to generate
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

    pip install faker.py

Download and copy
-----------------
``faker.py`` is the sole, self-contained module of the package. It includes
tests too. If it's more convenient to you, you could simply download the
``faker.py`` module and include it in your repository.

Since tests are included, it won't have a negative impact on your test
coverage (you might need to apply tweaks to your coverage configuration).

Usage
=====

.. code-block:: python

    from faker import Faker

    FAKER = Faker()

    # Generate a random word
    print(faker.word())

    # Generate a random sentence
    print(faker.sentence())

    # Generate a random paragraph
    print(faker.paragraph())

    # ... and many more

API
===

Faker class
-----------

.. autoclass:: faker.Faker
    :members:

Functions
---------

- ``word() -> str``
    Returns a random word from the Zen of Python.

- ``words(nb: int = 5) -> list[str]``
    Returns a list of 'nb' random words from the Zen of Python.

- ``sentence(nb_words: int = 5) -> str``
    Returns a random sentence with 'nb_words' number of words.

- ``paragraph(nb_sentences: int = 5) -> str``
    Returns a random paragraph with 'nb_sentences' number of sentences.

- ``paragraphs(nb: int = 3) -> str``
    Returns 'nb' number of random paragraphs.

- ``text(nb_chars: int = 200) -> str``
    Returns random text with up to 'nb_chars' characters.

- ``file_name(extension: str = "txt") -> str``
    Returns a random file name with the given extension.

- ``email(domain: str = "example.com") -> str``
    Returns a random email with the specified domain.

- ``url(protocols: Optional[tuple[str]] = None, tlds: Optional[tuple[str]] = None, suffixes: Optional[tuple[str]] = None) -> str``
    Returns a random URL.

- ``pyint(min_value: int = 0, max_value: int = 9999) -> int``
    Returns a random integer between 'min_value' and 'max_value'.

- ``pybool() -> bool``
    Returns a random boolean value.

- ``pystr(nb_chars=20) -> str``
    Returns a random string of 'nb_chars' length.

- ``pyfloat(min_value: float = 0.0, max_value: float = 10.0) -> float``
    Returns a random float between 'min_value' and 'max_value'.

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
``faker.py`` is modeled after the famous `Faker`_ package. Its' API is highly 
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
