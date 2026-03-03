Project source-tree
===================

Below is the layout of the project (to 10 levels), followed by
the contents of each key file.

.. code-block:: text
   :caption: Project directory layout

   fake.py/
   ├── fakepy
   │   └── __init__.py
   ├── .coveralls.yml
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

README.rst
----------

.. literalinclude:: ../README.rst
   :language: rst
   :caption: README.rst

CONTRIBUTING.rst
----------------

.. literalinclude:: ../CONTRIBUTING.rst
   :language: rst
   :caption: CONTRIBUTING.rst

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

SECURITY.md
-----------

.. literalinclude:: ../SECURITY.md
   :language: markdown
   :caption: SECURITY.md

conftest.py
-----------

.. literalinclude:: ../conftest.py
   :language: python
   :caption: conftest.py

fake.py
-------

.. literalinclude:: ../fake.py
   :language: python
   :caption: fake.py
   :end-before: # ******************** Tests *********************

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
