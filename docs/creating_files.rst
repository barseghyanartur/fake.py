Creating files
==============

.. Internal references

.. _fake.py: https://github.com/barseghyanartur/fake.py/
.. _Creating archives: https://fakepy.readthedocs.io/en/latest/creating_archives.html
.. _Creating DOCX: https://fakepy.readthedocs.io/en/latest/creating_docx.html
.. _Creating images: https://fakepy.readthedocs.io/en/latest/creating_images.html
.. _Creating ODT: https://fakepy.readthedocs.io/en/latest/creating_odt.html
.. _Creating PDF: https://fakepy.readthedocs.io/en/latest/creating_pdf.html

Creation of specific file formats is extensively covered in dedicated
sections:

- `Creating archives`_
- `Creating DOCX`_
- `Creating images`_
- `Creating ODT`_
- `Creating PDF`_

This section covers basic concepts of file generation within `fake.py`_.

It's possible to generate either bytes or files on the file system.

- When generating bytes, the returned value is ``BytesValue``.
- When generating files on the file system, the returned value
  is ``StringValue``.

Both ``BytesValue`` and ``StringValue`` behave like ``bytes`` and ``str``
respectively, but have a ``data`` (``dict``) property, which contains useful
meta-data about the specific kind of file.

For generated files, it will always have the following:

- ``storage``: Storage class that was used to generate the file.
- ``filename``: Absolute file path. It's important to know, that string
  representation of the file contains a relative file path.

----

See the example below for a **graphic** PDF generation:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_pdf_file
        :emphasize-lines: 3

        from fake import FAKER

        pdf_file = FAKER.pdf_file()

        print(pdf_file)  # Relative path
        # tmp/tmpnvwoa2ap.pdf

        print(pdf_file.data["filename"])  # Absolute path
        # /tmp/tmp/tmpnvwoa2ap.pdf

        print(pdf_file.data)  # Meta-data
        # {'storage': <fake.FileSystemStorage at 0x7f72221fd750>,
        #  'filename': '/tmp/tmp/tmpragc8wyr.pdf',
        #  'content': None}

----

See the example below for a **text** PDF generation:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_text_pdf_file
        :emphasize-lines: 3

        from fake import FAKER

        pdf_file = FAKER.text_pdf_file()

        print(pdf_file)
        # tmp/tmpragc8wyr.pdf

        print(pdf_file.data["filename"])
        # /tmp/tmp/tmpragc8wyr.pdf

        print(pdf_file.data)
        # {'storage': <fake.FileSystemStorage at 0x7f7222157750>,
        #  'filename': '/tmp/tmp/tmpragc8wyr.pdf',
        #  'content': 'If dutch beats although complex.'}

Note, that text PDF does contain full text of the entire document in the
``content`` key.

----
