Release history and notes
=========================

`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.3
---
2023-12-03

- Added factories.
- Added mechanism to clean-up (remove) the created test files.
- Improved documentation.

0.2
---
2023-12-01

- Add factories.
- Improve docs.
- Add ``uuid``, ``slug`` and ``username`` generators.
- Change ``date_between`` to ``date``.
- Change ``date_time_between`` to ``date_time``.

0.1.3
-----
2023-11-28

- Added ``pdf_file``, ``docx_file``, ``png_file``, ``svg_file``, ``bmp_file``,
  ``gif_file`` support.
- Added storages.

0.1.2
-----
2023-11-26

- Adding ``texts`` support.
- Improve tests and documentation.

0.1.1
-----
2023-11-26

- Adding ``DOCX`` support.
- Fixes in documentation.

0.1
---
2023-11-25

- Initial beta release.
