Creating archives
=================
.. External references

.. _faker-file: https://pypi.org/project/faker-file/

Creating archives for testing could be a challenging job. The goal of this
library is to help you out with basic tasks. You can easily generate ZIP
and TAR archives with 100 of files inside (supported by this package) or
even generate EML files (which are also considered archives, since they do
hold attachments).

If you don't like the quality of the generated files and want to have more
control over the content of the files, check the `faker-file`_ package,
which offers similar functionality but can produce complex documents with
almost no limitation of the content.

Supported image formats
-----------------------
Currently, 3 formats are supported:

- ``ZIP``
- ``TAR``
- ``EML``

ZIP
---
Creating a simple ZIP archive as bytes is as simple as follows:

.. code-block:: python
    :name: test_simple_zip_archive

    from fake import FAKER

    FAKER.zip()

The generated ZIP archive will consist of a single ``TXT`` with little text.

All customisation options are passed through the ``options`` optional argument,
which is a (nested) dictionary with the following keys:

- ``count`` (``int``):
- ``create_inner_file_func`` (``callable``):
- ``create_inner_file_args`` (``dict[str, Any]``):
- ``directory`` (``str``):

----

To customise the number of files in the archive, use the ``count`` key of
the ``options`` argument:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_zip_archive_nb_files_5
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.zip(options={"count": 5})

This will create a ``ZIP`` archive with 5 ``TXT`` files.

----

To customise the type of files in the archive, use
the ``create_inner_file_func`` key of the ``options`` argument:

.. code-block:: python
    :name: test_zip_archive_3_docx_file

    from fake import FAKER, create_inner_docx_file

    FAKER.zip(
        options={
            "create_inner_file_func": create_inner_docx_file,
        }
    )

This will create a ``ZIP`` archive with a single ``DOCX`` file.

----

All arguments of the ``create_inner_file_func`` are passed in
the ``create_inner_file_args`` argument:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_zip_archive_1_docx_file_with_given_texts
        :emphasize-lines: 3-

        from fake import FAKER, create_inner_docx_file

        FAKER.zip(
            options={
                "create_inner_file_func": create_inner_docx_file,
                "create_inner_file_args": {
                     "texts": ["There", "are", "no", "limits"],
                }
            }
        )

This will create a ``ZIP`` archive with single ``DOCX`` file of 4 pages, where
each of the given words ("There", "are", "no", "limits") would occupy a single
page.

----

There's no depth in terms of nesting:

.. code-block:: python
    :name: test_zip_archive_nested_zip

    from fake import (
        FAKER,
        create_inner_zip_file,
        create_inner_docx_file,
    )

    FAKER.zip(
        options={
            "count": 3,
            "create_inner_file_func": create_inner_zip_file,
            "create_inner_file_args": {
                "options": {
                    "count": 5,
                    "create_inner_file_func": create_inner_docx_file,
                    "create_inner_file_args": {
                       "nb_pages": 100,
                    }
                }
            }
        }
    )

This will create a nested ``ZIP`` archive with 3 ``ZIP`` archives in it,
each having 5 ``DOCX`` files of 100 pages each.

----

If you need consistent structure of mixed file types, see this:

.. code-block:: python
    :name: test_zip_archive_structured_using_list_create

    from fake import (
        FAKER,
        create_inner_docx_file,
        create_inner_txt_file,
        list_create_inner_file,
    )

    FAKER.zip(
        options={
            "create_inner_file_func": list_create_inner_file,
            "create_inner_file_args": {
                "func_list": [
                    (
                        create_inner_docx_file,
                        {"basename": "doc"},
                    ),
                    (
                        create_inner_txt_file,
                        {"basename": "doc_metadata"},
                    ),
                    (
                        create_inner_txt_file,
                        {"basename": "doc_isbn"},
                    ),
                ],
            },
        }
    )

This will create a ``ZIP`` archive with 1 ``DOCX`` file
named `doc.docx` and 2 ``TXT`` files named `doc_metadata.txt`
and `doc_isbn.txt`.

----

If you need a file on a disk, instead of bytes, use ``FAKER.zip_file`` instead.

.. container:: jsphinx-toggle-emphasis

   .. code-block:: python
        :name: test_zip_archive_file
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.zip_file()

----

All customisation options of ``zip`` are also applicable to ``zip_file``.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_zip_archive_file_structured_using_list_create
        :emphasize-lines: 8-

        from fake import (
            FAKER,
            create_inner_docx_file,
            create_inner_txt_file,
            list_create_inner_file,
        )

        FAKER.zip(
            options={
                "create_inner_file_func": list_create_inner_file,
                "create_inner_file_args": {
                    "func_list": [
                        (
                            create_inner_docx_file,
                            {"basename": "doc"},
                        ),
                        (
                            create_inner_txt_file,
                            {"basename": "doc_metadata"},
                        ),
                        (
                            create_inner_txt_file,
                            {"basename": "doc_isbn"},
                        ),
                    ],
                },
            }
        )

----

TAR
---
Works very similar to `ZIP`_. Use ``FAKER.tar`` and ``FAKER.tar_file`` instead
of ``FAKER.zip`` and ``FAKER.zip_file``.

EML
---
Works very similar to `ZIP`_. Use ``FAKER.eml`` and ``FAKER.eml_file`` instead
of ``FAKER.zip`` and ``FAKER.zip_file``.

- ``options``: (Optional) options. Similar to ``ZIP`` options.
- ``content``: (Optional) content of the email file.
- ``subject``: (Optional) subject of the email file.

Creating a simple EML archive as bytes is as simple as follows:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_simple_eml_archive
        :emphasize-lines: 3

        from fake import FAKER

        FAKER.eml()

----

This will create a ``EML`` archive with 1 ``DOCX`` file
named `doc.docx` and 2 ``TXT`` files named `doc_metadata.txt`
and `doc_isbn.txt`.

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_eml_archive_structured_using_list_create
        :emphasize-lines: 8-

        from fake import (
            FAKER,
            create_inner_docx_file,
            create_inner_txt_file,
            list_create_inner_file,
        )

        FAKER.eml(
            options={
                "create_inner_file_func": list_create_inner_file,
                "create_inner_file_args": {
                    "func_list": [
                        (
                            create_inner_docx_file,
                            {"basename": "doc"},
                        ),
                        (
                            create_inner_txt_file,
                            {"basename": "doc_metadata"},
                        ),
                        (
                            create_inner_txt_file,
                            {"basename": "doc_isbn"},
                        ),
                    ],
                },
            }
        )

----

Using text templates:

.. code-block:: python
    :name: test_text_templates

    from fake import FAKER, StringTemplate

    template = """
    {date(start_date='-7d')}
    {name}
    {sentence(nb_words=2, suffix='')} {pyint(min_value=1, max_value=99)}
    {randomise_string(value='#### ??', digits='123456789')} {city}

    Dear friend,

    {text(nb_chars=1000, allow_overflow=True)}

    Sincerely yours,

    {name}
    {email}
    {domain_name}
    """
    # EML file
    eml_file = FAKER.eml_file(content=StringTemplate(template))
