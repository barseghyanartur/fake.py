Factories
=========

Django example
--------------
**factories.py**

.. code-block:: python

    from django.conf import settings
    from fake import (
        DjangoModelFactory,
        Factory,
        FileSystemStorage,
        SubFactory,
        pre_save,
    )

    from article.models import Article

    STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")

    class ArticleFactory(DjangoModelFactory):
        title = Factory.sentence()
        slug = Factory.slug()
        content = Factory.text()
        image = Factory.png_file(storage=STORAGE)
        pub_date = Factory.date()
        safe_for_work = Factory.pybool()
        minutes_to_read = Factory.pyint(min_value=1, max_value=10)
        author = SubFactory(UserFactory)

        class Meta:
            model = Article

**Usage example**

.. code-block:: python

    article = ArticleFactory()  # Create one article
    articles = ArticleFactory.create_batch(5)  # Create 5 articles

Pydantic example
----------------

.. code-block:: python

    from pathlib import Path

    from fake import Factory, FileSystemStorage, ModelFactory, SubFactory

    from article.models import Article

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"
    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

    class ArticleFactory(ModelFactory):
        id = Factory.pyint()
        title = Factory.sentence()
        slug = Factory.slug()
        content = Factory.text()
        image = Factory.png_file(storage=STORAGE)
        pub_date = Factory.date()
        safe_for_work = Factory.pybool()
        minutes_to_read = Factory.pyint(min_value=1, max_value=10)
        author = SubFactory(UserFactory)

        class Meta:
            model = Article

*Used just like in previous example.*

TortoiseORM example
-------------------

.. code-block:: python

    from pathlib import Path

    from fake import Factory, FileSystemStorage, SubFactory, TortoiseModelFactory

    from article.models import Article, User

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"

    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

    class ArticleFactory(TortoiseModelFactory):
        id = Factory.pyint()
        title = Factory.sentence()
        slug = Factory.slug()
        content = Factory.text()
        image = Factory.png_file(storage=STORAGE)
        pub_date = Factory.date_time()
        safe_for_work = Factory.pybool()
        minutes_to_read = Factory.pyint(min_value=1, max_value=10)
        author = SubFactory(UserFactory)

        class Meta:
            model = Article

*Used just like in previous example.*
