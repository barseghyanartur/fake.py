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

    # Generate random first name
    FAKER.first_name()

    # Generate random last name
    FAKER.last_name()

    # Generate random name
    FAKER.name()

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
.. class:: Faker

    faker.py - simplified, standalone alternative with no dependencies.

    .. method:: first_name()

        Returns a random first name.

    .. method:: last_name()

        Returns a random last name.

    .. method:: name()

        Returns a random full name.

    .. method:: word()

        Returns a random word from the Zen of Python.

    .. method:: words(nb: int = 5)

        Returns a list of 'nb' random words from the Zen of Python.

    .. method:: sentence(nb_words: int = 5)

        Returns a random sentence with 'nb_words' number of words.

    .. method:: sentences(nb: int = 3)

        Returns 'nb' number of random sentences.

    .. method:: paragraph(nb_sentences: int = 5)

        Returns a random paragraph with 'nb_sentences' number of sentences.

    .. method:: paragraphs(nb: int = 3)

        Returns 'nb' number of random paragraphs.

    .. method:: text(nb_chars: int = 200)

        Returns random text with up to 'nb_chars' characters.

    .. method:: file_name(extension: str = "txt")

        Returns a random file name with the given extension.

    .. method:: email(domain: str = "example.com")

        Returns a random email with the specified domain.

    .. method:: url(
            protocols: Optional[tuple[str]] = None,
            tlds: Optional[tuple[str]] = None,
            suffixes: Optional[tuple[str]] = None
        )

        Returns a random URL.

    .. method:: pyint(min_value: int = 0, max_value: int = 9999)

        Returns a random integer between 'min_value' and 'max_value'.

    .. method:: pybool()

        Returns a random boolean value.

    .. method:: pystr(nb_chars=20)

        Returns a random string of 'nb_chars' length.

    .. method:: pyfloat(min_value: float = 0.0, max_value: float = 10.0)

        Returns a random float between 'min_value' and 'max_value'.

    .. method:: ipv4()

        Returns a random IPv4 address.

    .. method:: date_between(start_date: str, end_date: str = "+0d")

        Generates a random date between `start_date` and `end_date`.

    .. method:: date_time_between(start_date: str, end_date: str = "+0d")

        Generates a random datetime between `start_date` and `end_date`.

    .. method:: pdf(
            nb_pages: int = 1,
            generator: Union[Type[TextPdfGenerator],
            Type[GraphicPdfGenerator]] = GraphicPdfGenerator, **kwargs
        )

        Creates a PDF document.

    .. method:: image(
            image_format: Literal["png", "svg", "bmp", "gif"] = "png",
            width: int = 100, height: int = 100,
            color: Tuple[int, int, int] = (0, 0, 255)
        )

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
