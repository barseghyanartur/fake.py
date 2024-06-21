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

0.7.3
-----
2024-06-21

.. note::

    Release dedicated to my dear son Tigran, who turned 12 today.

- Add ``text_pdf`` and ``text_pdf_file`` providers, which are shortcuts for
  ``pdf`` and ``pdf_file`` with ``generator`` set to ``TextPdfGenerator``.
- Allow to optionally tag providers.
- Tag all implemented providers.

0.7.2
-----
2024-06-17

- Add basic ``slugify`` function.
- Minor fixes in ``free_email`` and ``company_email`` providers.

0.7.1
-----
2024-06-11

- Test against SQLModel. Also included SQLModel examples.
- Improve docs.

0.7
---
2024-06-09

.. note::

    This release contains minor backwards incompatible changes. Namely,
    in the ``email`` provider.

- The ``domain`` (type: ``str``, default value: ``example.com``) argument
  of the ``email`` provider has been dropped in favour
  of ``domain_names`` (type: ``Optional[Tuple[str]``, default value: ``None``).
- Added a dedicated ``PydanticModelFactory`` (yet equal to ``ModelFactory``)
  for future improvements.
- Added ``PreInit`` factory class and ``pre_init`` decorator.
- Improved documentation of factories.
- Added ``random_choice`` and ``random_sample`` providers.
- Added ``tld``, ``domain_name``, ``free_email_domain``, ``company_email``
  and ``free_email`` providers.

0.6.9
-----
2024-05-10

- Minor fixes in ``pdf_file`` and ``docx_file`` providers.
- Minor fixes in docs.

0.6.8
-----
2024-05-06

- Minor fixes in docs.

0.6.7
-----
2024-01-17

- Add ``uuids``, ``first_names``, ``last_names``, ``names``, ``usernames`` and
  ``slugs`` plural providers (return ``List``).

0.6.6
-----
2024-01-15

- Add ``image_url`` provider.

0.6.5
-----
2023-12-18

- Improve docs.
- MyPy fixes.

0.6.4
-----
2023-12-16

- Add ``PreSave`` and ``PostSave``.

0.6.3
-----
2023-12-13

- Add ``LazyAttribute`` and ``LazyFunction``.
- Improve package portability (tests).
- Improve tests.

0.6.2
-----
2023-12-11

- Add ``SQLAlchemyModelFactory``.

0.6.1
-----
2023-12-10

- Allow to load registered ``Faker`` instance by ``uid`` or ``alias``.
- Improve test coverage.

0.6
---
2023-12-09

- Add optional argument ``alias`` to the ``Faker`` class.
- Improve multiple ``Faker`` instances.
- Add ``generic_file`` provider.

0.5
---
2023-12-08

- Make ``fake.Faker`` and ``fake.Factory`` classes more customizable.
- Introduce ``provider`` decorator to decorate provider methods.
- Documentation improvements.

0.4.1
-----
2023-12-07

- Added ``pydecimal``.
- Make ``date_time`` timezone aware.
- Added documentation on how to customize.

0.4
---
2023-12-06

- Streamline on how to use traits, pre- and post-save hooks.

0.3.1
-----
2023-12-04

- Improve Tortoise ORM factory.
- Add traits.
- Improve docmentation.

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
