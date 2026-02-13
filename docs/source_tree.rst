Project source-tree
===================

Below is the layout of the project (to 10 levels), followed by
the contents of each key file.

.. code-block:: text
   :caption: Project directory layout

   fake.py/
   ├── docs
   │   ├── cheatsheet.rst
   │   ├── cli.rst
   │   ├── conf.py
   │   ├── contributor_guidelines.rst
   │   ├── creating_archives.rst
   │   ├── creating_docx.rst
   │   ├── creating_files.rst
   │   ├── creating_images.rst
   │   ├── creating_odt.rst
   │   ├── creating_pdf.rst
   │   ├── customisation.rst
   │   ├── customization.rst
   │   ├── documentation.rst
   │   ├── factories.rst
   │   ├── fake.rst
   │   ├── index.rst
   │   ├── llms.rst
   │   ├── package.rst
   │   ├── recipes.rst
   │   ├── seed.rst
   │   └── test_configuration_tweaks.rst
   ├── examples
   │   ├── customisation
   │   │   ├── address
   │   │   │   ├── __init__.py
   │   │   │   ├── factories.py
   │   │   │   ├── models.py
   │   │   │   └── tests.py
   │   │   ├── band
   │   │   │   ├── __init__.py
   │   │   │   ├── factories.py
   │   │   │   ├── models.py
   │   │   │   └── tests.py
   │   │   ├── __init__.py
   │   │   ├── address_cli.py
   │   │   ├── band_cli.py
   │   │   ├── custom_data_cli.py
   │   │   ├── data.py
   │   │   ├── fake_address.py
   │   │   ├── fake_band.py
   │   │   ├── manage.py
   │   │   ├── override_default_data.py
   │   │   ├── pyproject.toml
   │   │   └── README.rst
   │   ├── dataclasses
   │   │   ├── article
   │   │   │   ├── __init__.py
   │   │   │   ├── factories.py
   │   │   │   ├── models.py
   │   │   │   └── tests.py
   │   │   ├── media
   │   │   │   └── tmp
   │   │   ├── manage.py
   │   │   ├── pyproject.toml
   │   │   └── README.rst
   │   ├── django
   │   │   ├── article
   │   │   │   ├── migrations
   │   │   │   │   ├── 0001_initial.py
   │   │   │   │   └── __init__.py
   │   │   │   ├── __init__.py
   │   │   │   ├── admin.py
   │   │   │   ├── apps.py
   │   │   │   ├── factories.py
   │   │   │   ├── models.py
   │   │   │   └── tests.py
   │   │   ├── blog
   │   │   │   ├── __init__.py
   │   │   │   ├── asgi.py
   │   │   │   ├── settings.py
   │   │   │   ├── urls.py
   │   │   │   └── wsgi.py
   │   │   ├── media
   │   │   │   └── tmp
   │   │   ├── manage.py
   │   │   ├── pyproject.toml
   │   │   ├── README.rst
   │   │   └── requirements.in
   │   ├── hypothesis
   │   │   ├── manage.py
   │   │   ├── pyproject.toml
   │   │   ├── README.rst
   │   │   ├── requirements.in
   │   │   └── tests.py
   │   ├── lazyfuzzy
   │   │   ├── article
   │   │   │   ├── __init__.py
   │   │   │   ├── factories.py
   │   │   │   ├── models.py
   │   │   │   └── tests.py
   │   │   ├── media
   │   │   │   └── tmp
   │   │   ├── manage.py
   │   │   ├── pyproject.toml
   │   │   └── README.rst
   │   ├── pydantic
   │   │   ├── article
   │   │   │   ├── __init__.py
   │   │   │   ├── factories.py
   │   │   │   ├── models.py
   │   │   │   └── tests.py
   │   │   ├── media
   │   │   │   └── tmp
   │   │   ├── manage.py
   │   │   ├── pyproject.toml
   │   │   ├── README.rst
   │   │   └── requirements.in
   │   ├── sqlalchemy
   │   │   ├── article
   │   │   │   ├── __init__.py
   │   │   │   ├── factories.py
   │   │   │   ├── models.py
   │   │   │   └── tests.py
   │   │   ├── media
   │   │   │   └── tmp
   │   │   ├── config.py
   │   │   ├── conftest.py
   │   │   ├── manage.py
   │   │   ├── pyproject.toml
   │   │   ├── README.rst
   │   │   └── requirements.in
   │   ├── sqlmodel
   │   │   ├── article
   │   │   │   ├── __init__.py
   │   │   │   ├── factories.py
   │   │   │   ├── models.py
   │   │   │   └── tests.py
   │   │   ├── media
   │   │   │   └── tmp
   │   │   ├── config.py
   │   │   ├── conftest.py
   │   │   ├── manage.py
   │   │   ├── pyproject.toml
   │   │   ├── README.rst
   │   │   └── requirements.in
   │   ├── tortoise
   │   │   ├── article
   │   │   │   ├── __init__.py
   │   │   │   ├── factories.py
   │   │   │   ├── models.py
   │   │   │   └── tests.py
   │   │   ├── media
   │   │   │   └── tmp
   │   │   ├── conftest.py
   │   │   ├── manage.py
   │   │   ├── pyproject.toml
   │   │   ├── README.rst
   │   │   └── requirements.in
   │   ├── _pyproject.toml
   │   └── README.rst
   ├── fakepy
   │   └── __init__.py
   ├── .coveralls.yml
   ├── __copy_fake.py
   ├── CODE_OF_CONDUCT.md
   ├── conftest.py
   ├── CONTRIBUTING.rst
   ├── fake.py
   ├── Makefile
   ├── MANIFEST.in
   ├── pyproject.toml
   ├── README.rst
   ├── SECURITY.md
   └── tox.ini

.coveralls.yml
--------------

.. literalinclude:: ../.coveralls.yml
   :language: yaml
   :caption: .coveralls.yml

CODE_OF_CONDUCT.md
------------------

.. literalinclude:: ../CODE_OF_CONDUCT.md
   :language: markdown
   :caption: CODE_OF_CONDUCT.md

CONTRIBUTING.rst
----------------

.. literalinclude:: ../CONTRIBUTING.rst
   :language: rst
   :caption: CONTRIBUTING.rst

README.rst
----------

.. literalinclude:: ../README.rst
   :language: rst
   :caption: README.rst

SECURITY.md
-----------

.. literalinclude:: ../SECURITY.md
   :language: markdown
   :caption: SECURITY.md

__copy_fake.py
--------------

.. literalinclude:: ../__copy_fake.py
   :language: python
   :caption: __copy_fake.py

conftest.py
-----------

.. literalinclude:: ../conftest.py
   :language: python
   :caption: conftest.py

docs/_static/examples/creating_docx/docx_bytes_1.py
---------------------------------------------------

.. literalinclude:: _static/examples/creating_docx/docx_bytes_1.py
   :language: python
   :caption: docs/_static/examples/creating_docx/docx_bytes_1.py

docs/_static/examples/creating_docx/docx_bytes_2.py
---------------------------------------------------

.. literalinclude:: _static/examples/creating_docx/docx_bytes_2.py
   :language: python
   :caption: docs/_static/examples/creating_docx/docx_bytes_2.py

docs/_static/examples/creating_docx/docx_bytes_3.py
---------------------------------------------------

.. literalinclude:: _static/examples/creating_docx/docx_bytes_3.py
   :language: python
   :caption: docs/_static/examples/creating_docx/docx_bytes_3.py

docs/_static/examples/creating_docx/docx_file_1.py
--------------------------------------------------

.. literalinclude:: _static/examples/creating_docx/docx_file_1.py
   :language: python
   :caption: docs/_static/examples/creating_docx/docx_file_1.py

docs/_static/examples/creating_docx/docx_file_2.py
--------------------------------------------------

.. literalinclude:: _static/examples/creating_docx/docx_file_2.py
   :language: python
   :caption: docs/_static/examples/creating_docx/docx_file_2.py

docs/_static/examples/creating_docx/docx_file_3.py
--------------------------------------------------

.. literalinclude:: _static/examples/creating_docx/docx_file_3.py
   :language: python
   :caption: docs/_static/examples/creating_docx/docx_file_3.py

docs/_static/examples/creating_images/png_bytes_1.py
----------------------------------------------------

.. literalinclude:: _static/examples/creating_images/png_bytes_1.py
   :language: python
   :caption: docs/_static/examples/creating_images/png_bytes_1.py

docs/_static/examples/creating_images/png_bytes_2.py
----------------------------------------------------

.. literalinclude:: _static/examples/creating_images/png_bytes_2.py
   :language: python
   :caption: docs/_static/examples/creating_images/png_bytes_2.py

docs/_static/examples/creating_images/png_file_1.py
---------------------------------------------------

.. literalinclude:: _static/examples/creating_images/png_file_1.py
   :language: python
   :caption: docs/_static/examples/creating_images/png_file_1.py

docs/_static/examples/creating_images/png_file_2.py
---------------------------------------------------

.. literalinclude:: _static/examples/creating_images/png_file_2.py
   :language: python
   :caption: docs/_static/examples/creating_images/png_file_2.py

docs/_static/examples/creating_odt/odt_bytes_1.py
-------------------------------------------------

.. literalinclude:: _static/examples/creating_odt/odt_bytes_1.py
   :language: python
   :caption: docs/_static/examples/creating_odt/odt_bytes_1.py

docs/_static/examples/creating_odt/odt_bytes_2.py
-------------------------------------------------

.. literalinclude:: _static/examples/creating_odt/odt_bytes_2.py
   :language: python
   :caption: docs/_static/examples/creating_odt/odt_bytes_2.py

docs/_static/examples/creating_odt/odt_bytes_3.py
-------------------------------------------------

.. literalinclude:: _static/examples/creating_odt/odt_bytes_3.py
   :language: python
   :caption: docs/_static/examples/creating_odt/odt_bytes_3.py

docs/_static/examples/creating_odt/odt_file_1.py
------------------------------------------------

.. literalinclude:: _static/examples/creating_odt/odt_file_1.py
   :language: python
   :caption: docs/_static/examples/creating_odt/odt_file_1.py

docs/_static/examples/creating_odt/odt_file_2.py
------------------------------------------------

.. literalinclude:: _static/examples/creating_odt/odt_file_2.py
   :language: python
   :caption: docs/_static/examples/creating_odt/odt_file_2.py

docs/_static/examples/creating_odt/odt_file_3.py
------------------------------------------------

.. literalinclude:: _static/examples/creating_odt/odt_file_3.py
   :language: python
   :caption: docs/_static/examples/creating_odt/odt_file_3.py

docs/_static/examples/creating_pdf/graphic_pdf_bytes_1.py
---------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/graphic_pdf_bytes_1.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/graphic_pdf_bytes_1.py

docs/_static/examples/creating_pdf/graphic_pdf_bytes_2.py
---------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/graphic_pdf_bytes_2.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/graphic_pdf_bytes_2.py

docs/_static/examples/creating_pdf/graphic_pdf_file_1.py
--------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/graphic_pdf_file_1.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/graphic_pdf_file_1.py

docs/_static/examples/creating_pdf/graphic_pdf_file_2.py
--------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/graphic_pdf_file_2.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/graphic_pdf_file_2.py

docs/_static/examples/creating_pdf/text_pdf_bytes_1.py
------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/text_pdf_bytes_1.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/text_pdf_bytes_1.py

docs/_static/examples/creating_pdf/text_pdf_bytes_2.py
------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/text_pdf_bytes_2.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/text_pdf_bytes_2.py

docs/_static/examples/creating_pdf/text_pdf_bytes_2b.py
-------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/text_pdf_bytes_2b.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/text_pdf_bytes_2b.py

docs/_static/examples/creating_pdf/text_pdf_bytes_3.py
------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/text_pdf_bytes_3.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/text_pdf_bytes_3.py

docs/_static/examples/creating_pdf/text_pdf_file_1.py
-----------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/text_pdf_file_1.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/text_pdf_file_1.py

docs/_static/examples/creating_pdf/text_pdf_file_2.py
-----------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/text_pdf_file_2.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/text_pdf_file_2.py

docs/_static/examples/creating_pdf/text_pdf_file_3.py
-----------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/text_pdf_file_3.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/text_pdf_file_3.py

docs/_static/examples/creating_pdf/text_pdf_file_django_1.py
------------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/text_pdf_file_django_1.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/text_pdf_file_django_1.py

docs/_static/examples/creating_pdf/text_pdf_file_pydantic_1.py
--------------------------------------------------------------

.. literalinclude:: _static/examples/creating_pdf/text_pdf_file_pydantic_1.py
   :language: python
   :caption: docs/_static/examples/creating_pdf/text_pdf_file_pydantic_1.py

docs/cheatsheet.rst
-------------------

.. literalinclude:: cheatsheet.rst
   :language: rst
   :caption: docs/cheatsheet.rst

docs/cli.rst
------------

.. literalinclude:: cli.rst
   :language: rst
   :caption: docs/cli.rst

docs/conf.py
------------

.. literalinclude:: conf.py
   :language: python
   :caption: docs/conf.py

docs/contributor_guidelines.rst
-------------------------------

.. literalinclude:: contributor_guidelines.rst
   :language: rst
   :caption: docs/contributor_guidelines.rst

docs/creating_archives.rst
--------------------------

.. literalinclude:: creating_archives.rst
   :language: rst
   :caption: docs/creating_archives.rst

docs/creating_docx.rst
----------------------

.. literalinclude:: creating_docx.rst
   :language: rst
   :caption: docs/creating_docx.rst

docs/creating_files.rst
-----------------------

.. literalinclude:: creating_files.rst
   :language: rst
   :caption: docs/creating_files.rst

docs/creating_images.rst
------------------------

.. literalinclude:: creating_images.rst
   :language: rst
   :caption: docs/creating_images.rst

docs/creating_odt.rst
---------------------

.. literalinclude:: creating_odt.rst
   :language: rst
   :caption: docs/creating_odt.rst

docs/creating_pdf.rst
---------------------

.. literalinclude:: creating_pdf.rst
   :language: rst
   :caption: docs/creating_pdf.rst

docs/customisation.rst
----------------------

.. literalinclude:: customisation.rst
   :language: rst
   :caption: docs/customisation.rst

docs/customization.rst
----------------------

.. literalinclude:: customization.rst
   :language: rst
   :caption: docs/customization.rst

docs/documentation.rst
----------------------

.. literalinclude:: documentation.rst
   :language: rst
   :caption: docs/documentation.rst

docs/factories.rst
------------------

.. literalinclude:: factories.rst
   :language: rst
   :caption: docs/factories.rst

docs/fake.rst
-------------

.. literalinclude:: fake.rst
   :language: rst
   :caption: docs/fake.rst

docs/index.rst
--------------

.. literalinclude:: index.rst
   :language: rst
   :caption: docs/index.rst

docs/llms.rst
-------------

.. literalinclude:: llms.rst
   :language: rst
   :caption: docs/llms.rst

docs/package.rst
----------------

.. literalinclude:: package.rst
   :language: rst
   :caption: docs/package.rst

docs/recipes.rst
----------------

.. literalinclude:: recipes.rst
   :language: rst
   :caption: docs/recipes.rst

docs/seed.rst
-------------

.. literalinclude:: seed.rst
   :language: rst
   :caption: docs/seed.rst

docs/test_configuration_tweaks.rst
----------------------------------

.. literalinclude:: test_configuration_tweaks.rst
   :language: rst
   :caption: docs/test_configuration_tweaks.rst

examples/README.rst
-------------------

.. literalinclude:: ../examples/README.rst
   :language: rst
   :caption: examples/README.rst

examples/_pyproject.toml
------------------------

.. literalinclude:: ../examples/_pyproject.toml
   :language: toml
   :caption: examples/_pyproject.toml

examples/customisation/README.rst
---------------------------------

.. literalinclude:: ../examples/customisation/README.rst
   :language: rst
   :caption: examples/customisation/README.rst

examples/customisation/__init__.py
----------------------------------

.. literalinclude:: ../examples/customisation/__init__.py
   :language: python
   :caption: examples/customisation/__init__.py

examples/customisation/address/__init__.py
------------------------------------------

.. literalinclude:: ../examples/customisation/address/__init__.py
   :language: python
   :caption: examples/customisation/address/__init__.py

examples/customisation/address/factories.py
-------------------------------------------

.. literalinclude:: ../examples/customisation/address/factories.py
   :language: python
   :caption: examples/customisation/address/factories.py

examples/customisation/address/models.py
----------------------------------------

.. literalinclude:: ../examples/customisation/address/models.py
   :language: python
   :caption: examples/customisation/address/models.py

examples/customisation/address/tests.py
---------------------------------------

.. literalinclude:: ../examples/customisation/address/tests.py
   :language: python
   :caption: examples/customisation/address/tests.py

examples/customisation/address_cli.py
-------------------------------------

.. literalinclude:: ../examples/customisation/address_cli.py
   :language: python
   :caption: examples/customisation/address_cli.py

examples/customisation/band/__init__.py
---------------------------------------

.. literalinclude:: ../examples/customisation/band/__init__.py
   :language: python
   :caption: examples/customisation/band/__init__.py

examples/customisation/band/factories.py
----------------------------------------

.. literalinclude:: ../examples/customisation/band/factories.py
   :language: python
   :caption: examples/customisation/band/factories.py

examples/customisation/band/models.py
-------------------------------------

.. literalinclude:: ../examples/customisation/band/models.py
   :language: python
   :caption: examples/customisation/band/models.py

examples/customisation/band/tests.py
------------------------------------

.. literalinclude:: ../examples/customisation/band/tests.py
   :language: python
   :caption: examples/customisation/band/tests.py

examples/customisation/band_cli.py
----------------------------------

.. literalinclude:: ../examples/customisation/band_cli.py
   :language: python
   :caption: examples/customisation/band_cli.py

examples/customisation/custom_data_cli.py
-----------------------------------------

.. literalinclude:: ../examples/customisation/custom_data_cli.py
   :language: python
   :caption: examples/customisation/custom_data_cli.py

examples/customisation/data.py
------------------------------

.. literalinclude:: ../examples/customisation/data.py
   :language: python
   :caption: examples/customisation/data.py

examples/customisation/fake_address.py
--------------------------------------

.. literalinclude:: ../examples/customisation/fake_address.py
   :language: python
   :caption: examples/customisation/fake_address.py

examples/customisation/fake_band.py
-----------------------------------

.. literalinclude:: ../examples/customisation/fake_band.py
   :language: python
   :caption: examples/customisation/fake_band.py

examples/customisation/manage.py
--------------------------------

.. literalinclude:: ../examples/customisation/manage.py
   :language: python
   :caption: examples/customisation/manage.py

examples/customisation/override_default_data.py
-----------------------------------------------

.. literalinclude:: ../examples/customisation/override_default_data.py
   :language: python
   :caption: examples/customisation/override_default_data.py

examples/customisation/pyproject.toml
-------------------------------------

.. literalinclude:: ../examples/customisation/pyproject.toml
   :language: toml
   :caption: examples/customisation/pyproject.toml

examples/dataclasses/README.rst
-------------------------------

.. literalinclude:: ../examples/dataclasses/README.rst
   :language: rst
   :caption: examples/dataclasses/README.rst

examples/dataclasses/article/__init__.py
----------------------------------------

.. literalinclude:: ../examples/dataclasses/article/__init__.py
   :language: python
   :caption: examples/dataclasses/article/__init__.py

examples/dataclasses/article/factories.py
-----------------------------------------

.. literalinclude:: ../examples/dataclasses/article/factories.py
   :language: python
   :caption: examples/dataclasses/article/factories.py

examples/dataclasses/article/models.py
--------------------------------------

.. literalinclude:: ../examples/dataclasses/article/models.py
   :language: python
   :caption: examples/dataclasses/article/models.py

examples/dataclasses/article/tests.py
-------------------------------------

.. literalinclude:: ../examples/dataclasses/article/tests.py
   :language: python
   :caption: examples/dataclasses/article/tests.py

examples/dataclasses/manage.py
------------------------------

.. literalinclude:: ../examples/dataclasses/manage.py
   :language: python
   :caption: examples/dataclasses/manage.py

examples/dataclasses/pyproject.toml
-----------------------------------

.. literalinclude:: ../examples/dataclasses/pyproject.toml
   :language: toml
   :caption: examples/dataclasses/pyproject.toml

examples/django/README.rst
--------------------------

.. literalinclude:: ../examples/django/README.rst
   :language: rst
   :caption: examples/django/README.rst

examples/django/article/__init__.py
-----------------------------------

.. literalinclude:: ../examples/django/article/__init__.py
   :language: python
   :caption: examples/django/article/__init__.py

examples/django/article/admin.py
--------------------------------

.. literalinclude:: ../examples/django/article/admin.py
   :language: python
   :caption: examples/django/article/admin.py

examples/django/article/apps.py
-------------------------------

.. literalinclude:: ../examples/django/article/apps.py
   :language: python
   :caption: examples/django/article/apps.py

examples/django/article/factories.py
------------------------------------

.. literalinclude:: ../examples/django/article/factories.py
   :language: python
   :caption: examples/django/article/factories.py

examples/django/article/migrations/0001_initial.py
--------------------------------------------------

.. literalinclude:: ../examples/django/article/migrations/0001_initial.py
   :language: python
   :caption: examples/django/article/migrations/0001_initial.py

examples/django/article/migrations/__init__.py
----------------------------------------------

.. literalinclude:: ../examples/django/article/migrations/__init__.py
   :language: python
   :caption: examples/django/article/migrations/__init__.py

examples/django/article/models.py
---------------------------------

.. literalinclude:: ../examples/django/article/models.py
   :language: python
   :caption: examples/django/article/models.py

examples/django/article/tests.py
--------------------------------

.. literalinclude:: ../examples/django/article/tests.py
   :language: python
   :caption: examples/django/article/tests.py

examples/django/blog/__init__.py
--------------------------------

.. literalinclude:: ../examples/django/blog/__init__.py
   :language: python
   :caption: examples/django/blog/__init__.py

examples/django/blog/asgi.py
----------------------------

.. literalinclude:: ../examples/django/blog/asgi.py
   :language: python
   :caption: examples/django/blog/asgi.py

examples/django/blog/settings.py
--------------------------------

.. literalinclude:: ../examples/django/blog/settings.py
   :language: python
   :caption: examples/django/blog/settings.py

examples/django/blog/urls.py
----------------------------

.. literalinclude:: ../examples/django/blog/urls.py
   :language: python
   :caption: examples/django/blog/urls.py

examples/django/blog/wsgi.py
----------------------------

.. literalinclude:: ../examples/django/blog/wsgi.py
   :language: python
   :caption: examples/django/blog/wsgi.py

examples/django/manage.py
-------------------------

.. literalinclude:: ../examples/django/manage.py
   :language: python
   :caption: examples/django/manage.py

examples/django/pyproject.toml
------------------------------

.. literalinclude:: ../examples/django/pyproject.toml
   :language: toml
   :caption: examples/django/pyproject.toml

examples/hypothesis/README.rst
------------------------------

.. literalinclude:: ../examples/hypothesis/README.rst
   :language: rst
   :caption: examples/hypothesis/README.rst

examples/hypothesis/manage.py
-----------------------------

.. literalinclude:: ../examples/hypothesis/manage.py
   :language: python
   :caption: examples/hypothesis/manage.py

examples/hypothesis/pyproject.toml
----------------------------------

.. literalinclude:: ../examples/hypothesis/pyproject.toml
   :language: toml
   :caption: examples/hypothesis/pyproject.toml

examples/hypothesis/tests.py
----------------------------

.. literalinclude:: ../examples/hypothesis/tests.py
   :language: python
   :caption: examples/hypothesis/tests.py

examples/lazyfuzzy/README.rst
-----------------------------

.. literalinclude:: ../examples/lazyfuzzy/README.rst
   :language: rst
   :caption: examples/lazyfuzzy/README.rst

examples/lazyfuzzy/article/__init__.py
--------------------------------------

.. literalinclude:: ../examples/lazyfuzzy/article/__init__.py
   :language: python
   :caption: examples/lazyfuzzy/article/__init__.py

examples/lazyfuzzy/article/factories.py
---------------------------------------

.. literalinclude:: ../examples/lazyfuzzy/article/factories.py
   :language: python
   :caption: examples/lazyfuzzy/article/factories.py

examples/lazyfuzzy/article/models.py
------------------------------------

.. literalinclude:: ../examples/lazyfuzzy/article/models.py
   :language: python
   :caption: examples/lazyfuzzy/article/models.py

examples/lazyfuzzy/article/tests.py
-----------------------------------

.. literalinclude:: ../examples/lazyfuzzy/article/tests.py
   :language: python
   :caption: examples/lazyfuzzy/article/tests.py

examples/lazyfuzzy/manage.py
----------------------------

.. literalinclude:: ../examples/lazyfuzzy/manage.py
   :language: python
   :caption: examples/lazyfuzzy/manage.py

examples/lazyfuzzy/pyproject.toml
---------------------------------

.. literalinclude:: ../examples/lazyfuzzy/pyproject.toml
   :language: toml
   :caption: examples/lazyfuzzy/pyproject.toml

examples/pydantic/README.rst
----------------------------

.. literalinclude:: ../examples/pydantic/README.rst
   :language: rst
   :caption: examples/pydantic/README.rst

examples/pydantic/article/__init__.py
-------------------------------------

.. literalinclude:: ../examples/pydantic/article/__init__.py
   :language: python
   :caption: examples/pydantic/article/__init__.py

examples/pydantic/article/factories.py
--------------------------------------

.. literalinclude:: ../examples/pydantic/article/factories.py
   :language: python
   :caption: examples/pydantic/article/factories.py

examples/pydantic/article/models.py
-----------------------------------

.. literalinclude:: ../examples/pydantic/article/models.py
   :language: python
   :caption: examples/pydantic/article/models.py

examples/pydantic/article/tests.py
----------------------------------

.. literalinclude:: ../examples/pydantic/article/tests.py
   :language: python
   :caption: examples/pydantic/article/tests.py

examples/pydantic/manage.py
---------------------------

.. literalinclude:: ../examples/pydantic/manage.py
   :language: python
   :caption: examples/pydantic/manage.py

examples/pydantic/pyproject.toml
--------------------------------

.. literalinclude:: ../examples/pydantic/pyproject.toml
   :language: toml
   :caption: examples/pydantic/pyproject.toml

examples/sqlalchemy/README.rst
------------------------------

.. literalinclude:: ../examples/sqlalchemy/README.rst
   :language: rst
   :caption: examples/sqlalchemy/README.rst

examples/sqlalchemy/article/__init__.py
---------------------------------------

.. literalinclude:: ../examples/sqlalchemy/article/__init__.py
   :language: python
   :caption: examples/sqlalchemy/article/__init__.py

examples/sqlalchemy/article/factories.py
----------------------------------------

.. literalinclude:: ../examples/sqlalchemy/article/factories.py
   :language: python
   :caption: examples/sqlalchemy/article/factories.py

examples/sqlalchemy/article/models.py
-------------------------------------

.. literalinclude:: ../examples/sqlalchemy/article/models.py
   :language: python
   :caption: examples/sqlalchemy/article/models.py

examples/sqlalchemy/article/tests.py
------------------------------------

.. literalinclude:: ../examples/sqlalchemy/article/tests.py
   :language: python
   :caption: examples/sqlalchemy/article/tests.py

examples/sqlalchemy/config.py
-----------------------------

.. literalinclude:: ../examples/sqlalchemy/config.py
   :language: python
   :caption: examples/sqlalchemy/config.py

examples/sqlalchemy/conftest.py
-------------------------------

.. literalinclude:: ../examples/sqlalchemy/conftest.py
   :language: python
   :caption: examples/sqlalchemy/conftest.py

examples/sqlalchemy/manage.py
-----------------------------

.. literalinclude:: ../examples/sqlalchemy/manage.py
   :language: python
   :caption: examples/sqlalchemy/manage.py

examples/sqlalchemy/pyproject.toml
----------------------------------

.. literalinclude:: ../examples/sqlalchemy/pyproject.toml
   :language: toml
   :caption: examples/sqlalchemy/pyproject.toml

examples/sqlmodel/README.rst
----------------------------

.. literalinclude:: ../examples/sqlmodel/README.rst
   :language: rst
   :caption: examples/sqlmodel/README.rst

examples/sqlmodel/article/__init__.py
-------------------------------------

.. literalinclude:: ../examples/sqlmodel/article/__init__.py
   :language: python
   :caption: examples/sqlmodel/article/__init__.py

examples/sqlmodel/article/factories.py
--------------------------------------

.. literalinclude:: ../examples/sqlmodel/article/factories.py
   :language: python
   :caption: examples/sqlmodel/article/factories.py

examples/sqlmodel/article/models.py
-----------------------------------

.. literalinclude:: ../examples/sqlmodel/article/models.py
   :language: python
   :caption: examples/sqlmodel/article/models.py

examples/sqlmodel/article/tests.py
----------------------------------

.. literalinclude:: ../examples/sqlmodel/article/tests.py
   :language: python
   :caption: examples/sqlmodel/article/tests.py

examples/sqlmodel/config.py
---------------------------

.. literalinclude:: ../examples/sqlmodel/config.py
   :language: python
   :caption: examples/sqlmodel/config.py

examples/sqlmodel/conftest.py
-----------------------------

.. literalinclude:: ../examples/sqlmodel/conftest.py
   :language: python
   :caption: examples/sqlmodel/conftest.py

examples/sqlmodel/manage.py
---------------------------

.. literalinclude:: ../examples/sqlmodel/manage.py
   :language: python
   :caption: examples/sqlmodel/manage.py

examples/sqlmodel/pyproject.toml
--------------------------------

.. literalinclude:: ../examples/sqlmodel/pyproject.toml
   :language: toml
   :caption: examples/sqlmodel/pyproject.toml

examples/tortoise/README.rst
----------------------------

.. literalinclude:: ../examples/tortoise/README.rst
   :language: rst
   :caption: examples/tortoise/README.rst

examples/tortoise/article/__init__.py
-------------------------------------

.. literalinclude:: ../examples/tortoise/article/__init__.py
   :language: python
   :caption: examples/tortoise/article/__init__.py

examples/tortoise/article/factories.py
--------------------------------------

.. literalinclude:: ../examples/tortoise/article/factories.py
   :language: python
   :caption: examples/tortoise/article/factories.py

examples/tortoise/article/models.py
-----------------------------------

.. literalinclude:: ../examples/tortoise/article/models.py
   :language: python
   :caption: examples/tortoise/article/models.py

examples/tortoise/article/tests.py
----------------------------------

.. literalinclude:: ../examples/tortoise/article/tests.py
   :language: python
   :caption: examples/tortoise/article/tests.py

examples/tortoise/conftest.py
-----------------------------

.. literalinclude:: ../examples/tortoise/conftest.py
   :language: python
   :caption: examples/tortoise/conftest.py

examples/tortoise/manage.py
---------------------------

.. literalinclude:: ../examples/tortoise/manage.py
   :language: python
   :caption: examples/tortoise/manage.py

examples/tortoise/pyproject.toml
--------------------------------

.. literalinclude:: ../examples/tortoise/pyproject.toml
   :language: toml
   :caption: examples/tortoise/pyproject.toml

fake.py
-------

.. literalinclude:: ../fake.py
   :language: python
   :caption: fake.py

fakepy/__init__.py
------------------

.. literalinclude:: ../fakepy/__init__.py
   :language: python
   :caption: fakepy/__init__.py

pyproject.toml
--------------

.. literalinclude:: ../pyproject.toml
   :language: toml
   :caption: pyproject.toml
