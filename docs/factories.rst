Factories
=========

Django example
--------------
**article/models.py**

.. code-block:: python

    from django.conf import settings
    from django.db import models
    from django.utils import timezone

    class Article(models.Model):
        title = models.CharField(max_length=255)
        slug = models.SlugField(unique=True)
        content = models.TextField()
        image = models.ImageField(null=True, blank=True)
        pub_date = models.DateTimeField(default=timezone.now)
        safe_for_work = models.BooleanField(default=False)
        minutes_to_read = models.IntegerField(default=5)
        author = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )

        def __str__(self):
            return self.title

**article/factories.py**

.. code-block:: python

    from django.conf import settings
    from django.contrib.auth.models import User
    from fake import (
        FACTORY,
        DjangoModelFactory,
        FileSystemStorage,
        SubFactory,
        pre_save,
    )

    from article.models import Article

    STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")


    class UserFactory(DjangoModelFactory):

        username = FACTORY.username()
        first_name = FACTORY.first_name()
        last_name = FACTORY.last_name()
        email = FACTORY.email()
        last_login = FACTORY.date_time()
        is_superuser = False
        is_staff = False
        is_active = FACTORY.pybool()
        date_joined = FACTORY.date_time()

        class Meta:
            model = User
            get_or_create = ("username",)

        @staticmethod
        @pre_save
        def __set_password(instance):
            instance.set_password("test")


    class ArticleFactory(DjangoModelFactory):

        title = FACTORY.sentence()
        slug = FACTORY.slug()
        content = FACTORY.text()
        image = FACTORY.png_file(storage=STORAGE)
        pub_date = FACTORY.date()
        safe_for_work = FACTORY.pybool()
        minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
        author = SubFactory(UserFactory)

        class Meta:
            model = Article


**Usage example**

.. code-block:: python

    # Create one article
    article = ArticleFactory()

    # Create 5 articles
    articles = ArticleFactory.create_batch(5)

    # Create one article with authors username set to admin.
    article = ArticleFactory(author__username="admin")

Pydantic example
----------------

.. code-block:: python

    from pathlib import Path

    from fake import FACTORY, FileSystemStorage, ModelFactory, SubFactory

    from article.models import Article, User

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"

    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

    class UserFactory(ModelFactory):
        id = FACTORY.pyint()
        username = FACTORY.username()
        first_name = FACTORY.first_name()
        last_name = FACTORY.last_name()
        email = FACTORY.email()
        last_login = FACTORY.date_time()
        is_superuser = False
        is_staff = False
        is_active = FACTORY.pybool()
        date_joined = FACTORY.date_time()

        class Meta:
            model = User

    class ArticleFactory(ModelFactory):
        id = FACTORY.pyint()
        title = FACTORY.sentence()
        slug = FACTORY.slug()
        content = FACTORY.text()
        image = FACTORY.png_file(storage=STORAGE)
        pub_date = FACTORY.date()
        safe_for_work = FACTORY.pybool()
        minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
        author = SubFactory(UserFactory)

        class Meta:
            model = Article

*Used just like in previous example.*

TortoiseORM example
-------------------

.. code-block:: python

    from pathlib import Path

    from fake import FACTORY, FileSystemStorage, SubFactory, TortoiseModelFactory

    from article.models import Article, User

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"

    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

    class UserFactory(TortoiseModelFactory):
        """User factory."""

        # id = FACTORY.pyint()
        username = FACTORY.username()
        first_name = FACTORY.first_name()
        last_name = FACTORY.last_name()
        email = FACTORY.email()
        last_login = FACTORY.date_time()
        is_superuser = False
        is_staff = False
        is_active = FACTORY.pybool()
        date_joined = FACTORY.date_time()

        class Meta:
            model = User
            get_or_create = ("username",)

    class ArticleFactory(TortoiseModelFactory):
        """Article factory."""

        # id = FACTORY.pyint()
        title = FACTORY.sentence()
        slug = FACTORY.slug()
        content = FACTORY.text()
        image = FACTORY.png_file(storage=STORAGE)
        pub_date = FACTORY.date_time()
        safe_for_work = FACTORY.pybool()
        minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
        author = SubFactory(UserFactory)

        class Meta:
            model = Article

*Used just like in previous example.*

Dataclasses example
-------------------
.. code-block:: python

    from pathlib import Path

    from fake import FACTORY, FileSystemStorage, ModelFactory, SubFactory

    from article.models import Article, User

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"

    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

    class UserFactory(ModelFactory):
        id = FACTORY.pyint()
        username = FACTORY.username()
        first_name = FACTORY.first_name()
        last_name = FACTORY.last_name()
        email = FACTORY.email()
        last_login = FACTORY.date_time()
        is_superuser = False
        is_staff = False
        is_active = FACTORY.pybool()
        date_joined = FACTORY.date_time()

        class Meta:
            model = User

    class ArticleFactory(ModelFactory):
        id = FACTORY.pyint()
        title = FACTORY.sentence()
        slug = FACTORY.slug()
        content = FACTORY.text()
        image = FACTORY.png_file(storage=STORAGE)
        pub_date = FACTORY.date()
        safe_for_work = FACTORY.pybool()
        minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
        author = SubFactory(UserFactory)

        class Meta:
            model = Article
