Factories
=========

- ``pre_init`` is a method decorator that will always run before the instance
  is initialised.
- ``pre_save`` is a method decorator that will always run before the instance
  is saved.
- ``post_save`` is a method decorator that will always run after the instance
  is saved.
- ``trait`` decorator runs the code if set to True in factory constructor.
- ``PreInit`` is like the ``pre_init`` decorator of the ``ModelFactory``,
  but you can pass arguments to it and have a lot of flexibility. See
  a working example (below) of how set a user password in Django.
- ``PreSave`` is like the ``pre_save`` decorator of the ``ModelFactory``,
  but you can pass arguments to it and have a lot of flexibility. See
  a working example (below) of how set a user password in Django.
- ``PostSave`` is like the ``post_save`` decorator of the ``ModelFactory``,
  but you can pass arguments to it and have a lot of flexibility. See a
  working example (below) of how to assign a User to a Group after
  User creation.
- ``LazyAttribute`` expects a callable, will take the instance as a first
  argument, runs it with extra arguments specified and sets the value as
  an attribute name.
- ``LazyFunction`` expects a callable, runs it (without any arguments) and
  sets the value as an attribute name.
- ``SubFactory`` is for specifying relations (typically - ForeignKeys or
  nested objects).

Django example
--------------
Models
~~~~~~
In the ``Django`` example, we will be using ``User`` and ``Group`` models from
``django.contrib.auth`` sub-package. The ``Article`` would be the only
application specific custom model.

*Filename: article/models.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/django/article/models.py
        :language: python
        :lines: 1-3, 9-26

    *See the full example*
    :download:`here <_static/examples/factories/django/article/models.py>`

----

Factories
~~~~~~~~~

Factory for the Django's built-in ``Group`` model could look as simple as this:

*Filename: article/factories.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/django/article/factories.py
        :language: python
        :lines: 4-5, 7, 10-11, 13, 23, 56-58, 68-72

    *See the full example*
    :download:`here <_static/examples/factories/django/article/factories.py>`

----

Factory for the Django's built-in ``User`` model could look as this:

*Filename: article/factories.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/django/article/factories.py
        :language: python
        :lines: 1-2, 4, 6-10, 12, 15-17, 23, 73-90, 121-135, 141-146

    *See the full example*
    :download:`here <_static/examples/factories/django/article/factories.py>`

Breakdown:

- ``username`` is a required field. We shouldn't be using ``PreSave``
  or ``PostSave`` methods here, because we need it to be available and resolved
  before calling the class constructor (missing required fields would fail on
  Pydantic and other frameworks that enforce strong type checking). That's why
  ``PreInit``, which operates on the ``dict`` level, from which the model
  instance is constructed, is used here to construct the ``username`` value
  from ``first_name`` and the ``last_name``. The ``set_username`` helper
  function, which is used by ``PreInit``, accepts a dictionary with model data
  as argument and all changes to that dictionary are passed further to the
  class constructor. It's important to mention that functions passed to the
  ``PreInit``, do hot have to return anything.
- ``password`` is a non-required field and since Django has a well working way
  for setting it, use of ``PreSave`` is the best option here. It's important
  to mention that functions passed to the ``PreSave``, do hot have to return
  anything.
- ``group`` is a non-required many-to-many relationship. We need a User
  instance to be created before we can add User to a Group. That's why
  ``PostSave`` is best option here. It's important to mention that functions
  passed to the ``PostSave``, do hot have to return anything.

----

Factory for the the ``Artice`` model could look as this:

*Filename: article/factories.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/django/article/factories.py
        :language: python
        :lines: 3, 10, 14, 18, 20, 23-25, 35-55, 157-163, 180-198

    *See the full example*
    :download:`here <_static/examples/factories/django/article/factories.py>`

Breakdown:

- ``headline`` is a required field that should be available and resolved
  before the class constructor is called. We already know that ``PreInit``
  should be used for such cases. The ``headline`` value is constructed from
  ``content``.
- ``author`` is a foreign key relation field to the ``User`` model. For
  foreign key relations ``SubFactory`` is our best choice.
- ``image`` is a file field. Files created shall be placed in the path
  specified in ``MEDIA_ROOT`` Django setting. That's why we create
  and configure the ``STORAGE`` instance to pass it to ``FACTORY.png_file``
  in a ``storage`` argument.
- ``auto_minutes_to_read`` is a required field of the ``Article`` model.
  It needs to be resolved and available before the constructor class is
  called. That's the ``@pre_init`` decorator is used on
  the ``set_auto_minutes_read`` helper method.

----

All together it would look as follows:

*Filename: article/factories.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/django/article/factories.py
        :language: python
        :lines: 1-25, 35-58, 68-90, 121-135, 141-146, 157-163, 180-199

    *See the full example*
    :download:`here <_static/examples/factories/django/article/factories.py>`

----

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

----

Pydantic example
----------------
Models
~~~~~~
Example Pydantic models closely resemble the earlier shown Django models.

*Filename: article/models.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/pydantic/article/models.py
        :language: python
        :lines: 1-5, 15-25, 31-

    *See the full example*
    :download:`here <_static/examples/factories/pydantic/article/models.py>`

----

Factories
~~~~~~~~~
Example Pydantic factories are almost identical to the earlier shown Django
factories.

*Filename: article/factories.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/pydantic/article/factories.py
        :language: python
        :lines: 1-20, 30-98, 114-140

    *See the full example*
    :download:`here <_static/examples/factories/pydantic/article/factories.py>`

*Used just like in previous example.*

----

TortoiseORM example
-------------------
Models
~~~~~~
Example TortoiseORM models closely resemble the earlier shown Django models.

*Filename: article/models.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/tortoise/article/models.py
        :language: python
        :lines: 1-5, 15-21, 25-41, 45-61

    *See the full example*
    :download:`here <_static/examples/factories/tortoise/article/models.py>`

----

Factories
~~~~~~~~~
Example TortoiseORM factories are almost identical to the earlier shown Django
factories.

*Filename: article/factories.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/tortoise/article/factories.py
        :language: python
        :lines: 1-21, 31-106, 116-143

    *See the full example*
    :download:`here <_static/examples/factories/tortoise/article/factories.py>`

*Used just like in previous example.*

----

Dataclasses example
-------------------
Models
~~~~~~
Example dataclass models closely resemble the earlier shown Django models.

*Filename: article/models.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/dataclasses/article/models.py
        :language: python
        :lines: 1-5, 15-

    *See the full example*
    :download:`here <_static/examples/factories/dataclasses/article/models.py>`

----

Factories
~~~~~~~~~
Example dataclass factories are almost identical to the earlier shown Django
factories.

*Filename: article/factories.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/dataclasses/article/factories.py
        :language: python
        :lines: 1-20, 30-98, 109-135

    *See the full example*
    :download:`here <_static/examples/factories/dataclasses/article/factories.py>`

*Used just like in previous example.*

----

SQLAlchemy example
------------------
Configuration
~~~~~~~~~~~~~

*Filename: config.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/sqlalchemy/config.py
        :language: python
        :lines: 1-2, 12-

    *See the full example*
    :download:`here <_static/examples/factories/sqlalchemy/config.py>`

----

Models
~~~~~~
Example SQLAlchemy models closely resemble the earlier shown Django models.

*Filename: article/models.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/sqlalchemy/article/models.py
        :language: python
        :lines: 1-16, 26-46, 50-75, 79-105

    *See the full example*
    :download:`here <_static/examples/factories/sqlalchemy/article/models.py>`

----

Factories
~~~~~~~~~
Example SQLAlchemy factories are almost identical to the earlier shown Django
factories.

*Filename: article/factories.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/sqlalchemy/article/factories.py
        :language: python
        :lines: 1-21, 30-122, 133-163

    *See the full example*
    :download:`here <_static/examples/factories/sqlalchemy/article/factories.py>`

*Used just like in previous example.*

----

SQLModel example
----------------
Configuration
~~~~~~~~~~~~~

*Filename: config.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/sqlmodel/config.py
        :language: python
        :lines: 1-2, 12-

    *See the full example*
    :download:`here <_static/examples/factories/sqlmodel/config.py>`

----

Models
~~~~~~
Example SQLModel models closely resemble the earlier shown Django models.

*Filename: article/models.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/sqlmodel/article/models.py
        :language: python
        :lines: 1-5, 15-

    *See the full example*
    :download:`here <_static/examples/factories/sqlmodel/article/models.py>`

----

Factories
~~~~~~~~~
Example SQLModel factories are identical to the earlier shown SQLAlchemy
factories.

*Filename: article/factories.py*

.. container:: jsphinx-download

    .. literalinclude:: _static/examples/factories/sqlmodel/article/factories.py
        :language: python
        :lines: 1-21, 31-

    *See the full example*
    :download:`here <_static/examples/factories/sqlmodel/article/factories.py>`

*Used just like in previous example.*
