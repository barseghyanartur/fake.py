Seed
====

The following providers have consistent results when using seed:

- first_name
- first_names
- last_name
- last_names
- name
- names
- username
- usernames
- slug
- slugs
- word
- words
- sentence
- sentences
- paragraph
- paragraphs
- text
- texts
- dir_path
- file_extension
- mime_type
- tld
- domain_name
- free_email_domain
- email
- emails
- company_email
- company_emails
- free_email
- free_emails
- url
- image_url
- pyint
- pybool
- pystr
- pyfloat
- pydecimal
- ipv4
- date
- year
- time
- city
- country
- geo_location
- country_code
- locale
- latitude
- longitude
- latitude_longitude
- iban
- isbn10
- isbn13
- random_choice
- random_sample
- randomise_string
- string_template

If you need to seed, it's recommended to create yet another instance of Faker
to avoid possible collisions.

.. code-block:: python
    :name: test_seed

    from fake import Faker

    FAKER = Faker()

You could then do as follows:

.. continue: test_seed
.. code-block:: python
    :name: test_seed_2

    FAKER.seed(42)
    l1 = [FAKER.pyint(), FAKER.pyint(), FAKER.pyint(), FAKER.pyint()]

    FAKER.seed(42)
    l2 = [FAKER.pyint(), FAKER.pyint(), FAKER.pyint(), FAKER.pyint()]

    assert l1 == l2
