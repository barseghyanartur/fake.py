Factories
=========

- ``pre_save`` is a method decorator that will always run before the instance
  is saved.
- ``post_save`` is a method decorator that will always run after the instance
  is saved.
- ``trait`` decorator runs the code if set to True in factory constructor.
- ``PreSave`` is like the ``pre_save`` decorator of the ``ModelFactory``,
  but you can pass arguments to it and have a lot of flexibility. See
  a working example (below) of how set a user password in Django.
- ``PostSave`` is like the ``post_save`` decorator of the ``ModelFactory``,
  but you can pass arguments to it and have a lot of flexibility. See a
  working example (below) of how to assign a user to a Group after
  user creation.
- ``LazyAttribute`` expects a callable, will take the instance as a first
  argument, runs it with extra arguments specified and sets the value as
  an attribute name.
- ``LazyFunction`` expects a callable, runs it (without any arguments) and
  sets the value as an attribute name.
- ``SubFactory`` is for specifying relations (typically - ForeignKeys).

Django example
--------------
**article/models.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/django/article/models.py
        :language: python
        :lines: 1-3, 9-23

    *See the full example*
    :download:`here <_static/examples/factories/django/article/models.py>`

**article/factories.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/django/article/factories.py
        :language: python
        :lines: 1-21, 31-120, 130-162

    *See the full example*
    :download:`here <_static/examples/factories/django/article/factories.py>`

**Usage example**

.. code-block:: python

    # Create one article
    article = ArticleFactory()

    # Create 5 articles
    articles = ArticleFactory.create_batch(5)

    # Create one article with authors username set to admin.
    article = ArticleFactory(author__username="admin")

    # Using trait
    user = UserFactory(is_admin_user=True)

    # Using trait in SubFactory
    article = ArticleFactory(author__is_admin_user=True)

    # Create a user. Created user will automatically have his password
    # set to "test1234" and will be added to the group "Test group".
    user = UserFactory()

    # Create a user with custom password
    user = UserFactory(
        password=PreSave(set_password, password="another-pass"),
    )

    # Add a user to another group
    user = UserFactory(
        group=PostSave(add_to_group, name="Another group"),
    )

    # Or even add user to multiple groups at once
    user = UserFactory(
        group_1=PostSave(add_to_group, name="Another group"),
        group_2=PostSave(add_to_group, name="Yet another group"),
    )

Pydantic example
----------------
**article/models.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/pydantic/article/models.py
        :language: python
        :lines: 1-5, 15-

    *See the full example*
    :download:`here <_static/examples/factories/pydantic/article/models.py>`

**article/factories.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/pydantic/article/factories.py
        :language: python
        :lines: 1-15, 25-72, 83-98

    *See the full example*
    :download:`here <_static/examples/factories/pydantic/article/factories.py>`

*Used just like in previous example.*

TortoiseORM example
-------------------
**article/models.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/tortoise/article/models.py
        :language: python
        :lines: 1-5, 15-21, 25-41, 45-61

    *See the full example*
    :download:`here <_static/examples/factories/tortoise/article/models.py>`

**article/factories.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/tortoise/article/factories.py
        :language: python
        :lines: 1-16, 26-81, 91-106

    *See the full example*
    :download:`here <_static/examples/factories/tortoise/article/factories.py>`

*Used just like in previous example.*

Dataclasses example
-------------------
**article/models.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/dataclasses/article/models.py
        :language: python
        :lines: 1-5, 15-

    *See the full example*
    :download:`here <_static/examples/factories/dataclasses/article/models.py>`

**article/factories.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/dataclasses/article/factories.py
        :language: python
        :lines: 1-15, 25-72, 83-97

    *See the full example*
    :download:`here <_static/examples/factories/dataclasses/article/factories.py>`

*Used just like in previous example.*

SQLAlchemy example
------------------

**config.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/sqlalchemy/config.py
        :language: python
        :lines: 1-2, 12-

    *See the full example*
    :download:`here <_static/examples/factories/sqlalchemy/config.py>`

**article/models.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/sqlalchemy/article/models.py
        :language: python
        :lines: 1-15, 25-45, 49-74, 78-98

    *See the full example*
    :download:`here <_static/examples/factories/sqlalchemy/article/models.py>`

**article/factories.py**

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/sqlalchemy/article/factories.py
        :language: python
        :lines: 1-16, 25-96, 107-125

    *See the full example*
    :download:`here <_static/examples/factories/sqlalchemy/article/factories.py>`

*Used just like in previous example.*
