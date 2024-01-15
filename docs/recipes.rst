Recipes
=======
**Imports and initialization**

.. code-block:: python

    from fake import FAKER

----

**first_name**

Returns a random first name.

.. code-block:: python

    FAKER.first_name()

----

**last_name**

Returns a random last name.

.. code-block:: python

    FAKER.last_name()

----

**name**

Returns a random full name.

.. code-block:: python

    FAKER.name()

----

**word**

Returns a random word.

.. code-block:: python

    FAKER.word()

----

**words**

Returns a list of ``nb`` random words.

.. code-block:: python

    FAKER.words()

Arguments:

- ``nb`` (type: ``int``, default value: ``5``) is an optional argument.

Example with arguments (returns a list of 10 words):

.. code-block:: python

    FAKER.words(nb=10)

----

**sentence**

Returns a random sentence with ``nb_words`` number of words.

.. code-block:: python

    FAKER.sentence()

Arguments:

- ``nb_words`` (type: ``int``, default value: ``5``) is an optional argument.

Example with arguments (returns a sentence of 10 words):

.. code-block:: python

    FAKER.sentence(nb_words=10)

----

**sentences**

Returns ``nb`` number of random sentences.

.. code-block:: python

    FAKER.sentences()

Arguments:

- ``nb`` (type: ``int``, default value: ``3``) is an optional argument.

Example with arguments (returns a list of 10 sentences):

.. code-block:: python

    FAKER.sentences(nb=10)

----

**paragraph**

Returns a random paragraph with ``nb_sentences`` number of sentences.

.. code-block:: python

    FAKER.paragraph()

Arguments:

- ``nb_sentences`` (type: ``int``, default value: ``5``) is an optional
  argument.

Example with arguments (returns a paragraph of 10 sentences):

.. code-block:: python

    FAKER.paragraph(nb_sentences=10)

----

**paragraphs**

Returns ``nb`` number of random paragraphs.

.. code-block:: python

    FAKER.paragraphs()

Arguments:

- ``nb`` (type: ``int``, default value: ``3``) is an optional argument.

Example with arguments (returns a list of 10 paragraphs):

.. code-block:: python

    FAKER.paragraphs(nb=10)

----

**text**

Returns random text with up to ``nb_chars`` characters.

.. code-block:: python

    FAKER.text()

Arguments:

- ``nb_chars`` (type: ``int``, default value: ``200``) is an optional argument.

Example with arguments (returns a 1000 character long text):

.. code-block:: python

    FAKER.text(nb_chars=1_000)

----

**texts**

Returns ``nb`` number of random texts.

.. code-block:: python

    FAKER.texts()

Arguments:

- ``nb`` (type: ``int``, default value: ``3``) is an optional argument.

Example with arguments (returns a list of 10 texts):

.. code-block:: python

    FAKER.texts(nb=10)

----

**file_name**

Returns a random file name with the given extension.

.. code-block:: python

    FAKER.file_name()

Arguments:

- ``extension`` (type: ``str``, default value: ``txt``) is an optional
  argument.

Example with arguments (returns a filename with "png" extension):

.. code-block:: python

    FAKER.file_name(extension="png")

----

**email**

Returns a random email with the specified domain.

.. code-block:: python

    FAKER.email()

Arguments:

- ``domain`` (type: ``str``, default value: ``example.com``) is an optional
  argument.

Example with arguments (returns an email with "gmail.com" domain):

.. code-block:: python

    FAKER.email(domain="gmail.com")

----

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

----
**image_url**

Returns a valid random image URL.

.. code-block:: python

    FAKER.image_url()

Arguments:

- ``width`` (type: ``int``, default value: ``800``) is
  a required argument.
- ``height`` (type: ``int``, default value: ``600``) is
  an required argument.
- ``service_url`` (type: ``Optional[str]``, default value: ``None``) is
  an optional argument.

Example with arguments (alternative dimensions):

.. code-block:: python

    FAKER.image_url(width=640, height=480)

----

**pyint**

Returns a random integer between ``min_value`` and ``max_value``.

.. code-block:: python

    FAKER.pyint()

Arguments:

- ``min_value`` (type: ``int``, default value: ``0``) is an optional argument.
- ``max_value`` (type: ``int``, default value: ``9999``) is an optional
  argument.

Example with arguments (returns an integer between 0 and 100):

.. code-block:: python

    FAKER.pyint(min_value=0, max_value=100)

----

**pybool**

Returns a random boolean value.

.. code-block:: python

    FAKER.pybool()

----

**pystr**

Returns a random string of ``nb_chars`` length.

.. code-block:: python

    FAKER.pystr()

Arguments:

- ``nb_chars`` (type: ``int``, default value: ``20``) is an optional argument.

Example with arguments (returns a string of 64 characters):

.. code-block:: python

    FAKER.pystr(nb_chars=64)

----

**pyfloat**

Returns a random float between ``min_value`` and ``max_value``.

.. code-block:: python

    FAKER.pyfloat()

Arguments:

- ``min_value`` (type: ``float``, default value: ``0.0``) is an optional
  argument.
- ``max_value`` (type: ``float``, default value: ``10.00``) is an optional
  argument.

Example with arguments (returns a float between 0 and 100):

.. code-block:: python

    FAKER.pyfloat(min_value=0.0, max_value=100.0)

----

**pydecimal**

Returns a random decimal, according to given ``left_digits`` and
``right_digits``.

.. code-block:: python

    FAKER.pydecimal()

Arguments:

- ``left_digits`` (type: ``int``, default value: ``5``) is an optional
  argument.
- ``right_digits`` (type: ``int``, default value: ``2``) is an optional
  argument.
- ``positive`` (type: ``bool``, default value: ``True``) is an optional
  argument.

Example with arguments:

.. code-block:: python

    FAKER.pydecimal(left_digits=1, right_digits=4, positive=False)

----

**ipv4**

Returns a random IPv4 address.

.. code-block:: python

    FAKER.ipv4()

----

**date**

Generates a random date.

.. code-block:: python

    FAKER.date()

Arguments:

- ``start_date`` (type: ``str``, default value: ``-7d``) is a optional
  argument.
- ``end_date`` (type: ``str``, default value: ``+0d``) is an optional
  argument.

Example with arguments, generate a random date between given ``start_date``
and ``end_date``:

.. code-block:: python

    FAKER.date(start_date="-1d", end_date="+1d")

----

**date_time**

Generates a random datetime.

.. code-block:: python

    FAKER.date_time(start_date="-1d", end_date="+1d")

Arguments:

- ``start_date`` (type: ``str``, default value: ``-7d``) is an optional
  argument.
- ``end_date`` (type: ``str``, default value: ``+0d``) is an optional
  argument.

Example with arguments, generate a random date between given ``start_date``
and ``end_date``:

.. code-block:: python

    FAKER.date_time(start_date="-1d", end_date="+1d")

----

**pdf**

Generates a content (``bytes``) of a PDF document.

.. code-block:: python

    FAKER.pdf()

Arguments:

- ``nb_pages`` (type: ``int``, default value: ``1``) is an optional argument.
- ``texts`` (type: ``List[str]``, default value: ``None``) is an optional
  argument.
- ``generator``
  (type: ``Union[Type[TextPdfGenerator], Type[GraphicPdfGenerator]]``,
  default value: ``GraphicPdfGenerator``) is an optional argument.
- ``metadata`` (type: ``MetaData``, default value: ``None``) is an optional
  argument.

.. note::

    ``texts`` is valid only in case ``TextPdfGenerator`` is used.

.. note::

    Either ``nb_pages`` or ``texts`` shall be provided. ``nb_pages`` is by
    default set to ``1``, but if ``texts`` is given, the value of ``nb_pages``
    is adjusted accordingly.

Examples with arguments.

Generate a content (``bytes``) of a PDF document of 100 pages with random
graphics:

.. code-block:: python

    FAKER.pdf(nb_pages=100)

Generate a content (``bytes``) of a PDF document of 100 pages with random
texts:

.. code-block:: python

    from fake import TextPdfGenerator

    FAKER.pdf(nb_pages=100, generator=TextPdfGenerator)

If you want to get insights of the content used to generate the PDF (texts),
pass the ``metadata`` argument.

.. code-block:: python

    from fake import MetaData, TextPdfGenerator

    metadata = MetaData()
    FAKER.pdf(nb_pages=100, generator=TextPdfGenerator, metadata=metadata)

    print(metadata.data)  # Inspect ``metadata``

----

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

Example with arguments.

.. code-block:: python

    FAKER.image(
        image_format="svg",  # SVG format
        size=(640, 480),  # 640px width, 480px height
        color: (0, 0, 0),  # Fill rectangle with black
    )

----

**docx**

Generates a content (``bytes``) of a DOCX document.

.. code-block:: python

    FAKER.docx()

Arguments:

- ``nb_pages`` (type: ``int``, default value: ``1``) is an optional argument.
- ``texts`` (type: ``List[str]``, default value: ``None``) is an optional
  argument.

.. note::

    Either ``nb_pages`` or ``texts`` shall be provided. ``nb_pages`` is by
    default set to ``1``, but if ``texts`` is given, the value of ``nb_pages``
    is adjusted accordingly.

Examples with arguments.

Generate a content (``bytes``) of a DOCX document of 100 pages with random
texts:

.. code-block:: python

    FAKER.docx(nb_pages=100)

If you want to get insights of the content used to generate the DOCX (texts),
pass the ``metadata`` argument.

.. code-block:: python

    from fake import MetaData

    metadata = MetaData()
    FAKER.docx(nb_pages=100, metadata=metadata)

    print(metadata.data)  # Inspect ``metadata``

----

**pdf_file**

Generates a ``PDF`` file.

.. code-block:: python

    FAKER.pdf_file()

Arguments:

.. note::

    Accepts all arguments of ``pdf`` + the following:

- ``storage`` (type: ``BaseStorage``, default value: ``None``) is an optional
  argument.
- ``basename`` (type: ``str``, default value: ``None``) is an optional
  argument.
- ``prefix`` (type: ``str``, default value: ``None``) is an optional argument.

Examples with arguments.

Generate a PDF document of 100 pages with random graphics:

.. code-block:: python

    FAKER.pdf_file(nb_pages=100)

Generate a PDF document of 100 pages with random texts:

.. code-block:: python

    from fake import TextPdfGenerator

    FAKER.pdf_file(nb_pages=100, generator=TextPdfGenerator)

If you want to get insights of the content used to generate the PDF (texts),
pass the ``metadata`` argument.

.. code-block:: python

    from fake import MetaData, TextPdfGenerator

    metadata = MetaData()
    FAKER.pdf_file(nb_pages=100, generator=TextPdfGenerator, metadata=metadata)

    print(metadata.data)  # Inspect ``metadata``

----

**png_file**

Generates a ``PNG`` file.

.. code-block:: python

    FAKER.png_file()

Arguments:

.. note::

    Accepts all arguments of ``png`` + the following:

- ``storage`` (type: ``BaseStorage``, default value: ``None``) is an optional
  argument.
- ``basename`` (type: ``str``, default value: ``None``) is an optional
  argument.
- ``prefix`` (type: ``str``, default value: ``None``) is an optional argument.

Example with arguments.

.. code-block:: python

    FAKER.png_file(
        basename="png_file",  # Basename
        size=(640, 480),  # 640px width, 480px height
        color: (0, 0, 0),  # Fill rectangle with black
    )

----

**svg_file**

Generates an ``SVG`` file.

.. code-block:: python

    FAKER.svg_file()

Arguments:

.. note::

    Accepts all arguments of ``svg`` + the following:

- ``storage`` (type: ``BaseStorage``, default value: ``None``) is an optional
  argument.
- ``basename`` (type: ``str``, default value: ``None``) is an optional
  argument.
- ``prefix`` (type: ``str``, default value: ``None``) is an optional argument.

Example with arguments.

.. code-block:: python

    FAKER.svg_file(
        basename="svg_file",  # Basename
        size=(640, 480),  # 640px width, 480px height
        color: (0, 0, 0),  # Fill rectangle with black
    )

----

**bmp_file**

Generates a ``BMP`` file.

.. code-block:: python

    FAKER.bmp_file()

Arguments:

.. note::

    Accepts all arguments of ``bmp`` + the following:

- ``storage`` (type: ``BaseStorage``, default value: ``None``) is an optional
  argument.
- ``basename`` (type: ``str``, default value: ``None``) is an optional
  argument.
- ``prefix`` (type: ``str``, default value: ``None``) is an optional argument.

Example with arguments.

.. code-block:: python

    FAKER.bmp_file(
        basename="bmp_file",  # Basename
        size=(640, 480),  # 640px width, 480px height
        color: (0, 0, 0),  # Fill rectangle with black
    )

----

**gif_file**

Generates a ``GIF`` file.

.. code-block:: python

    FAKER.gif_file()

Arguments:

.. note::

    Accepts all arguments of ``gif`` + the following:

- ``storage`` (type: ``BaseStorage``, default value: ``None``) is an optional
  argument.
- ``basename`` (type: ``str``, default value: ``None``) is an optional
  argument.
- ``prefix`` (type: ``str``, default value: ``None``) is an optional argument.

Example with arguments.

.. code-block:: python

    FAKER.gif_file(
        basename="gif_file",  # Basename
        size=(640, 480),  # 640px width, 480px height
        color: (0, 0, 0),  # Fill rectangle with black
    )

----

**txt_file**

Generates a ``TXT`` file.

.. code-block:: python

    FAKER.txt_file()

Arguments:

.. note::

    Accepts all arguments of ``text`` + the following:

- ``storage`` (type: ``BaseStorage``, default value: ``None``) is an optional
  argument.
- ``basename`` (type: ``str``, default value: ``None``) is an optional
  argument.
- ``prefix`` (type: ``str``, default value: ``None``) is an optional argument.

Example with arguments.

.. code-block:: python

    FAKER.txt_file(
        basename="txt_file",  # Basename
        nb_chars=10_000,  # 10_000 characters long
    )
