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

Basics
------
It's possible to generate either in-memory byte content or actual files on the
file system.

- When generating bytes, the returned value is ``BytesValue``.
- When generating files on the file system, the returned value
  is ``StringValue``.

Both ``BytesValue`` and ``StringValue`` behave like ``bytes`` and ``str``
respectively, but have a ``data`` (``dict``) property, which contains useful
meta-data about the specific kind of file.

For generated files, it will always have the following:

- ``storage``: Storage class that was used to generate the file.
- ``filename``: Absolute file path. It's important to know that string
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

Clean up files
--------------
``FileSystemStorage`` is the default storage and by default files are stored
inside a ``tmp`` directory within the system's temporary directory, which is
commonly cleaned up after system restart. However, there's a mechanism of
cleaning up files after the tests run. At any time, to clean up all files
created by that moment, call ``clean_up`` method of the ``FileRegistry``
class instance, as shown below:

.. code-block:: python
    :name: test_file_registry

    from fake import FAKER, FILE_REGISTRY  # Import the file registry

    # Create a file
    txt_file = FAKER.txt_file()  # type: ``StringValue``
    filename = str(txt_file)  # Relative path to the file
    storage = txt_file.data["storage"]  # Storage instance

    # File should exist
    assert storage.exists(filename)

    # Trigger the clean-up
    FILE_REGISTRY.clean_up()

    # File no longer exists
    assert storage.exists(filename) is False

Typically you would call the ``clean_up`` method in the ``tearDown``.

----

To remove a single file, use the ``remove`` method of ``FileRegistry``
instance. In the example below, the file is removed by providing
the ``StringValue`` instance:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_file_registry_remove_by_string_value
        :emphasize-lines: 11-12

        from fake import FAKER, FILE_REGISTRY

        # Create a file
        txt_file = FAKER.txt_file()  # type: StringValue
        filename = str(txt_file)  # Relative path to the file
        storage = txt_file.data["storage"]  # Storage instance

        # File should exist
        assert storage.exists(filename)

        # Remove the file by providing the ``StringValue`` instance
        FILE_REGISTRY.remove(txt_file)

        # File no longer exists
        assert storage.exists(filename) is False

----

You can also remove by path. In the exampl below, the file is removed by
providing the ``str`` instance:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_file_registry_remove_by_str
        :emphasize-lines: 11-12

        from fake import FAKER, FILE_REGISTRY

        # Create a file
        txt_file = FAKER.txt_file()  # type: StringValue
        filename = str(txt_file)  # Relative path to the file
        storage = txt_file.data["storage"]  # Storage instance

        # File should exist
        assert storage.exists(filename)

        # Remove the file by providing the ``filename``
        FILE_REGISTRY.remove(filename)

        # File no longer exist
        assert storage.exists(filename) is False

----

If you only have a path to the file as ``str`` instance, you can find the
correspondent ``StringValue`` instance by searching, using the ``search``
method:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_file_registry_search
        :emphasize-lines: 11-12

        from fake import FAKER, FILE_REGISTRY

        # Create a file
        txt_file = FAKER.txt_file()  # type: ``StringValue``
        filename = str(txt_file)  # Relative path to the file
        storage = txt_file.data["storage"]  # Storage instance

        # File should exist
        assert storage.exists(filename)

        # Find the file by providing the ``str`` instance
        found_file = FILE_REGISTRY.search(filename)  # type: StringValue

        # They should be the same
        assert txt_file == found_file

----

.. raw:: html

    &nbsp;
