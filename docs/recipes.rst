Recipes
=======
.. _isbn-checker: https://isbn-checker.netlify.app/
.. _iban-calculator: https://www.ibancalculator.com/iban_validieren.html

Imports and initialization
--------------------------

.. code-block:: python
    :name: test_init

    from fake import FAKER

----

Providers
---------
first_name
~~~~~~~~~~

Returns a random first name.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_first_name
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.first_name()

----

last_name
~~~~~~~~~

Returns a random last name.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_last_name
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.last_name()

----

name
~~~~

Returns a random full name.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_name
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.name()

----

word
~~~~

Returns a random word.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_word
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.word()

----

words
~~~~~

Returns a list of ``nb`` random words.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_words
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.words()

Arguments:

- ``nb`` (type: ``int``, default value: ``5``) is an optional argument.

Example with arguments (returns a list of 10 words):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_words_nb_10
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.words(nb=10)

----

sentence
~~~~~~~~

Returns a random sentence with ``nb_words`` number of words.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_sentence
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.sentence()

Arguments:

- ``nb_words`` (type: ``int``, default value: ``5``) is an optional argument.

Example with arguments (returns a sentence of 10 words):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_sentence_nb_words_10
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.sentence(nb_words=10)

----

sentences
~~~~~~~~~

Returns ``nb`` number of random sentences.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_sentences
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.sentences()

Arguments:

- ``nb`` (type: ``int``, default value: ``3``) is an optional argument.

Example with arguments (returns a list of 10 sentences):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_sentences_nb_10
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.sentences(nb=10)

----

paragraph
~~~~~~~~~

Returns a random paragraph with ``nb_sentences`` number of sentences.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_paragraph
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.paragraph()

Arguments:

- ``nb_sentences`` (type: ``int``, default value: ``5``) is an optional
  argument.

Example with arguments (returns a paragraph of 10 sentences):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_paragraph_nb_sentences_10
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.paragraph(nb_sentences=10)

----

paragraphs
~~~~~~~~~~

Returns ``nb`` number of random paragraphs.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_paragraphs
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.paragraphs()

Arguments:

- ``nb`` (type: ``int``, default value: ``3``) is an optional argument.

Example with arguments (returns a list of 10 paragraphs):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_paragraphs_nb_10
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.paragraphs(nb=10)

----

text
~~~~

Returns random text with up to ``nb_chars`` characters.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_text
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.text()

Arguments:

- ``nb_chars`` (type: ``int``, default value: ``200``) is an optional argument.

Example with arguments (returns a 1000 character long text):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_text_nb_chars_1000
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.text(nb_chars=1_000)

----

texts
~~~~~

Returns ``nb`` number of random texts.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_texts
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.texts()

Arguments:

- ``nb`` (type: ``int``, default value: ``3``) is an optional argument.

Example with arguments (returns a list of 10 texts):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_texts_nb_10
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.texts(nb=10)

----

file_name
~~~~~~~~~

Returns a random file name with the given extension.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_file_name
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.file_name()

Arguments:

- ``extension`` (type: ``str``, default value: ``txt``) is an optional
  argument.

Example with arguments (returns a filename with "png" extension):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_file_name_extension_png
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.file_name(extension="png")

----

file_extension
~~~~~~~~~~~~~~

Returns a random file extension.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_file_extension
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.file_extension()

----

tld
~~~~~

Returns a TLD (top level domain name).

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_tld
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.tld()

Arguments:

- ``tlds`` (type: ``Optional[Tuple[str, ...]]``, default value: ``None``) is
  an optional argument.

Example with arguments (returns either "com", "net" or "org" TLD):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_tld_tlds_com_net_org
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.tld(tlds=("com", "net", "org"))

----

domain_name
~~~~~~~~~~~

Returns a domain name.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_domain_name
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.domain_name()

Arguments:

- ``tlds`` (type: ``Optional[Tuple[str, ...]]``, default value: ``None``) is
  an optional argument.

Example with arguments (returns an domain name with either "com", "net" or
"org" TLD):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_domain_name_tlds_com_net_org
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.domain_name(tlds=("com", "net", "org"))

----

free_email_domain
~~~~~~~~~~~~~~~~~

Returns a free e-mail domain name.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_free_email_domain
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.free_email_domain()

----

email
~~~~~

Returns a random email.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_email
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.email()

Arguments:

- ``domain_names`` (type: ``Optional[Tuple[str, ...]]``, default
  value: ``None``) is an optional argument.

Example with arguments (returns an email with either "gmail.com"
or "proton.me" domain):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_email_domain_gmail_proton
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.email(domain_names=("gmail.com", "proton.me"))

----

company_email
~~~~~~~~~~~~~

Returns a random company email.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_company_email
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.company_email()

Arguments:

- ``domain_names`` (type: ``Optional[Tuple[str, ...]]``, default
  value: ``None``) is an optional argument.

Example with arguments (returns an email with either "microsoft.com"
or "google.com" domain):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_company_email_domain_microsoft_google
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.email(domain_names=("microsoft.com", "google.com"))

----

free_email
~~~~~~~~~~

Returns a random free email.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_free_email
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.free_email()

Arguments:

- ``domain_names`` (type: ``Optional[Tuple[str, ...]]``, default
  value: ``None``) is an optional argument.

Example with arguments (returns an email with either "gmail.com"
or "proton.me" domain):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_free_email_domain_gmail_proton
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.email(domain_names=("gmail.com", "proton.me"))

----

url
~~~

Returns a random URL.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_url
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.url()

Arguments:

- ``protocols`` (type: ``Optional[Tuple[str]]``, default value: ``None``) is
  an optional argument.
- ``tlds`` (type: ``Optional[Tuple[str]]``, default value: ``None``) is
  an optional argument.
- ``suffixes`` (type: ``Optional[Tuple[str]]``, default value: ``None``) is
  an optional argument.

----

image_url
~~~~~~~~~

Returns a valid random image URL.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_image_url
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.image_url()

Arguments:

- ``width`` (type: ``int``, default value: ``800``) is
  a required argument.
- ``height`` (type: ``int``, default value: ``600``) is
  an required argument.
- ``service_url`` (type: ``Optional[str]``, default value: ``None``) is
  an optional argument.

Example with arguments (alternative dimensions):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_image_url_width_640_height_480
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.image_url(width=640, height=480)

----

pyint
~~~~~

Returns a random integer between ``min_value`` and ``max_value``.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pyint
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pyint()

Arguments:

- ``min_value`` (type: ``int``, default value: ``0``) is an optional argument.
- ``max_value`` (type: ``int``, default value: ``9999``) is an optional
  argument.

Example with arguments (returns an integer between 0 and 100):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pyint_min_value_0_max_value_100
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pyint(min_value=0, max_value=100)

----

pybool
~~~~~~

Returns a random boolean value.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pybool
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pybool()

----

pystr
~~~~~

Returns a random string of ``nb_chars`` length.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pystr
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pystr()

Arguments:

- ``nb_chars`` (type: ``int``, default value: ``20``) is an optional argument.

Example with arguments (returns a string of 64 characters):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pystr_nb_chars_64
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pystr(nb_chars=64)

----

pyfloat
~~~~~~~

Returns a random float between ``min_value`` and ``max_value``.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pyfloat
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pyfloat()

Arguments:

- ``min_value`` (type: ``float``, default value: ``0.0``) is an optional
  argument.
- ``max_value`` (type: ``float``, default value: ``10.00``) is an optional
  argument.

Example with arguments (returns a float between 0 and 100):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pyfloat_min_value_0_max_value_100
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pyfloat(min_value=0.0, max_value=100.0)

----

pydecimal
~~~~~~~~~

Returns a random decimal, according to given ``left_digits`` and
``right_digits``.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pydecimal
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pydecimal()

Arguments:

- ``left_digits`` (type: ``int``, default value: ``5``) is an optional
  argument.
- ``right_digits`` (type: ``int``, default value: ``2``) is an optional
  argument.
- ``positive`` (type: ``bool``, default value: ``True``) is an optional
  argument.

Example with arguments:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pydecimal_left_digits_1_right_digits_4_positive_false
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pydecimal(left_digits=1, right_digits=4, positive=False)

----

ipv4
~~~~

Returns a random IPv4 address.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_ipv4
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.ipv4()

----

date
~~~~

Generates a random date.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_date
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.date()

Arguments:

- ``start_date`` (type: ``str``, default value: ``-7d``) is a optional
  argument.
- ``end_date`` (type: ``str``, default value: ``+0d``) is an optional
  argument.

Example with arguments, generate a random date between given ``start_date``
and ``end_date``:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_date_start_date_end_date
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.date(start_date="-1d", end_date="+1d")

----

date_time
~~~~~~~~~

Generates a random datetime.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_date_time
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.date_time()

Arguments:

- ``start_date`` (type: ``str``, default value: ``-7d``) is an optional
  argument.
- ``end_date`` (type: ``str``, default value: ``+0d``) is an optional
  argument.

Example with arguments, generate a random date between given ``start_date``
and ``end_date``:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_date_time_start_date_end_date
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.date_time(start_date="-1d", end_date="+1d")

----

pdf
~~~

Generates a content (``bytes``) of a PDF document.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pdf
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pdf()

Arguments:

- ``nb_pages`` (type: ``int``, default value: ``1``) is an optional argument.
- ``texts`` (type: ``list[str]``, default value: ``None``) is an optional
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

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pdf_nb_pages_100
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pdf(nb_pages=100)

Generate a content (``bytes``) of a PDF document of 100 pages with random
texts:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pdf_nb_pages_100_generator_text
        :emphasize-lines: 2-

        from fake import FAKER
        from fake import TextPdfGenerator

        FAKER.pdf(nb_pages=100, generator=TextPdfGenerator)

If you want to get insights of the content used to generate the PDF (texts),
pass the ``metadata`` argument.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_nb_pages_100_generator_text_metadata
        :emphasize-lines: 2-

        from fake import FAKER
        from fake import MetaData, TextPdfGenerator

        metadata = MetaData()
        FAKER.pdf(nb_pages=100, generator=TextPdfGenerator, metadata=metadata)

        print(metadata.content)  # Inspect ``metadata``

----

image
~~~~~

Generates a content (``bytes``) of a image of the specified format and colour.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_image
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.image()  # Supported formats are `png`, `svg`, `bmp` and `gif`

Arguments:

- ``image_format`` (type: ``str``, default value: ``png``) is an optional
  argument.
- ``size`` (type: ``Tuple[int, int]``, default value: ``(100, 100)``) is an
  optional argument.
- ``color`` (type: ``Tuple[int, int, int]``, default value: ``(0, 0, 255)``)
  is an optional argument.

Example with arguments.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_image_image_format_svg
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.image(
            image_format="svg",  # SVG format
            size=(640, 480),  # 640px width, 480px height
            color=(0, 0, 0),  # Fill rectangle with black
        )

----

docx
~~~~

Generates a content (``bytes``) of a DOCX document.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_docx
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.docx()

Arguments:

- ``nb_pages`` (type: ``int``, default value: ``1``) is an optional argument.
- ``texts`` (type: ``list[str]``, default value: ``None``) is an optional
  argument.

.. note::

    Either ``nb_pages`` or ``texts`` shall be provided. ``nb_pages`` is by
    default set to ``1``, but if ``texts`` is given, the value of ``nb_pages``
    is adjusted accordingly.

Examples with arguments.

Generate a content (``bytes``) of a DOCX document of 100 pages with random
texts:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_docx_nb_pages_100
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.docx(nb_pages=100)

If you want to get insights of the content used to generate the DOCX (texts),
pass the ``metadata`` argument.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_docx_nb_pages_100_metadata
        :emphasize-lines: 2-

        from fake import FAKER
        from fake import MetaData

        metadata = MetaData()
        FAKER.docx(nb_pages=100, metadata=metadata)

        print(metadata.content)  # Inspect ``metadata``

----

odt
~~~

Generates a content (``bytes``) of a ODT document.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_odt
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.odt()

Arguments:

- ``nb_pages`` (type: ``int``, default value: ``1``) is an optional argument.
- ``texts`` (type: ``list[str]``, default value: ``None``) is an optional
  argument.

.. note::

    Either ``nb_pages`` or ``texts`` shall be provided. ``nb_pages`` is by
    default set to ``1``, but if ``texts`` is given, the value of ``nb_pages``
    is adjusted accordingly.

Examples with arguments.

Generate a content (``bytes``) of a ODT document of 100 pages with random
texts:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_odt_nb_pages_100
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.odt(nb_pages=100)

If you want to get insights of the content used to generate the ODT (texts),
pass the ``metadata`` argument.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_odt_nb_pages_100_metadata
        :emphasize-lines: 2-

        from fake import FAKER
        from fake import MetaData

        metadata = MetaData()
        FAKER.odt(nb_pages=100, metadata=metadata)

        print(metadata.content)  # Inspect ``metadata``

----

bin
~~~

Generates a content (``bytes``) of a BIN document.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_bin
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.bin()

Arguments:

- ``length`` (type: ``int``, default value: ``16``) is a required argument.

Examples with arguments.

Generate a content (``bytes``) of a BIN document of length 100:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_bin_length_100
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.bin(length=100)

----

zip
~~~

Generates a content (``bytes``) of a ZIP document.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_zip
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.zip()

Arguments:

- ``options`` (type: ``Dict``, default value: ``None``) is an optional argument.

----

eml
~~~

Generates a content (``bytes``) of a EML document.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_eml
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.eml()

Arguments:

- ``options`` (type: ``Dict``, default value: ``None``) is an optional argument.
- ``content`` (type: ``str``, default value: ``None``) is an optional argument.
- ``subject`` (type: ``str``, default value: ``None``) is an optional argument.

----

tar
~~~

Generates a content (``bytes``) of a TAR document.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_tar
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.tar()

Arguments:

- ``options`` (type: ``Dict``, default value: ``None``) is an optional argument.

----

pdf_file
~~~~~~~~

Generates a ``PDF`` file.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pdf_file
        :emphasize-lines: 3

        from fake import FAKER

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

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pdf_file_nb_pages_100
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.pdf_file(nb_pages=100)

Generate a PDF document of 100 pages with random texts:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pdf_file_nb_pages_100_generator_text
        :emphasize-lines: 2-

        from fake import FAKER
        from fake import TextPdfGenerator

        FAKER.pdf_file(nb_pages=100, generator=TextPdfGenerator)

If you want to get insights of the content used to generate the PDF (texts),
pass the ``metadata`` argument.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pdf_file_nb_pages_100_generator_text_metadata
        :emphasize-lines: 2-

        from fake import FAKER
        from fake import MetaData, TextPdfGenerator

        metadata = MetaData()
        FAKER.pdf_file(nb_pages=100, generator=TextPdfGenerator, metadata=metadata)

        print(metadata.content)  # Inspect ``metadata``

----

png_file
~~~~~~~~

Generates a ``PNG`` file.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_png_file
        :emphasize-lines: 3

        from fake import FAKER

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

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_png_file_basename_size_color
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.png_file(
            basename="png_file",  # Basename
            size=(640, 480),  # 640px width, 480px height
            color=(0, 0, 0),  # Fill rectangle with black
        )

----

svg_file
~~~~~~~~

Generates an ``SVG`` file.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_svg_file
        :emphasize-lines: 3

        from fake import FAKER

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

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_svg_file_basename_size_color
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.svg_file(
            basename="svg_file",  # Basename
            size=(640, 480),  # 640px width, 480px height
            color=(0, 0, 0),  # Fill rectangle with black
        )

----

bmp_file
~~~~~~~~

Generates a ``BMP`` file.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_bmp_file
        :emphasize-lines: 3

        from fake import FAKER

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

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_bmp_file_basename_size_color
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.bmp_file(
            basename="bmp_file",  # Basename
            size=(640, 480),  # 640px width, 480px height
            color=(0, 0, 0),  # Fill rectangle with black
        )

----

gif_file
~~~~~~~~

Generates a ``GIF`` file.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_gif_file
        :emphasize-lines: 3

        from fake import FAKER

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

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_gif_file_basename_size_color
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.gif_file(
            basename="gif_file",  # Basename
            size=(640, 480),  # 640px width, 480px height
            color=(0, 0, 0),  # Fill rectangle with black
        )

----

txt_file
~~~~~~~~

Generates a ``TXT`` file.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_txt_file
        :emphasize-lines: 3

        from fake import FAKER

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

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_txt_file_basename_nb_chars
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.txt_file(
            basename="txt_file",  # Basename
            nb_chars=10_000,  # 10_000 characters long
        )

----

city
~~~~
Get a random city.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_city
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.city()

----

country
~~~~~~~
Get a random country.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_country
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.country()

----

geo_location
~~~~~~~~~~~~
Get a random geo-location.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_geo_location
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.geo_location()

----

country_code
~~~~~~~~~~~~
Get a random country code.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_country_code
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.country_code()

----

locale
~~~~~~
Generate a random locale.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_locale
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.locale()

----

latitude
~~~~~~~~
Generate a random latitude.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_latitude
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.latitude()

----

longitude
~~~~~~~~~
Generate a random longitude.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_longitude
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.longitude()

----

latitude_longitude
~~~~~~~~~~~~~~~~~~
Generate a random (latitude, longitude) pair.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_latitude_longitude
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.latitude_longitude()

----

isbn10
~~~~~~
Generate a random ISBN10. Can be validated using `isbn-checker`_.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_isbn10
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.isbn10()

----

isbn13
~~~~~~
Generate a random ISBN13. Can be validated using `isbn-checker`_.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_isbn13
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.isbn13()

----

iban
~~~~
Generate a random IBAN. Can be validated using `iban-calculator`_.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_iban
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.iban()

----

random_choice
~~~~~~~~~~~~~

Picks a random element from the sequence given.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_random_choice
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.random_choice(("Art", "Photography", "Generative AI"))

----

random_sample
~~~~~~~~~~~~~

Picks a given number of random elements from the sequence given.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_random_sample
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.random_sample(("Art", "Photography", "Generative AI"), 2)

----

randomise_string
~~~~~~~~~~~~~~~~

Replaces placeholders in a given string with random letters and digits.

- Placeholders ``?`` are replaced by random uppercase letters.
- Placeholders ``#`` are replaced by random digits.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_randomise_string
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.randomise_string("???? ##")

----

Optional arguments:

- ``letters`` (type: ``str``, default value: ``string.ascii_uppercase``).
- ``digits`` (type: ``str``, default value: ``string.digits``).

Example with arguments.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_randomise_string_custom_args
        :emphasize-lines: 1, 3-

        import string
        from fake import FAKER

        FAKER.randomise_string(
            "???? ##",
            letters=string.ascii_letters,  # Use both upper- and lower-case
            digits="123456789",  # Exclude 0
        )

Sample output:

.. code-block:: text

    1234 Aa
