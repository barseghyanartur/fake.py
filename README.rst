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
    FAKER.word()

    # Generate random words
    FAKER.words()

    # Generate a random sentence
    FAKER.sentence()

    # Generate random sentences
    FAKER.sentences()

    # Generate a random paragraph
    FAKER.paragraph()

    # Generate random paragraphs
    FAKER.paragraphs()

    # Generate random text
    FAKER.text()

    # Generate random file name
    FAKER.file_name()

    # Generate random email
    FAKER.email()

    # Generate random URL
    FAKER.url()

    # Generate random integer
    FAKER.pyint()

    # Generate random boolean
    FAKER.pybool()

    # Generate random string
    FAKER.pystr()

    # Generate random float
    FAKER.pyfloat()

    # Generate random IPV4
    FAKER.ipv4()

    # Generate random date between given dates
    FAKER.date_between(start_date="-1d", end_date="+1d")

    # Generate random datetime between given datetimes
    FAKER.date_time_between(start_date="-1d", end_date="+1d")

    # Generate random PDF (bytes)
    FAKER.pdf()

    # Generate random image (bytes)
    FAKER.image()  # Supported formats are `png`, `svg`, `bmp` and `gif`

Methods
-------
- ``first_name() -> str``
    Returns a random first name.

- ``last_name() -> str``
    Returns a random last name.

- ``name() -> str``
    Returns a random full name.

- ``word() -> str``
    Returns a random word from the Zen of Python.

- ``words(nb: int = 5) -> list[str]``
    Returns a list of 'nb' random words from the Zen of Python.

- ``sentence(nb_words: int = 5) -> str``
    Returns a random sentence with 'nb_words' number of words.

- ``sentences(nb: int = 3) -> list[str]``
    Returns 'nb' number of random sentences.

- ``paragraph(nb_sentences: int = 5) -> str``
    Returns a random paragraph with 'nb_sentences' number of sentences.

- ``paragraphs(nb: int = 3) -> list[str]``
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

- ``ipv4() -> str``
    Returns a random IPv4 address.

- ``date_between(start_date: str, end_date: str = "+0d") -> date``
    Generates a random date between `start_date` and `end_date`.

- ``date_time_between(start_date: str, end_date: str = "+0d") -> datetime``
    Generates a random datetime between `start_date` and `end_date`.

- ``pdf(nb_pages: int = 1, generator: Union[Type[TextPdfGenerator], Type[GraphicPdfGenerator]] = GraphicPdfGenerator, **kwargs) -> bytes``
    Creates a PDF document.

- ``image(image_format: Literal["png", "svg", "bmp", "gif"] = "png", width: int = 100, height: int = 100, color: Tuple[int, int, int] = (0, 0, 255)) -> bytes``
    Creates an image in the specified format and color.

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
