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

    # For Django, all files shall be placed inside `MEDIA_ROOT` directory.
    # That's why you need to apply this trick - define a
    # custom `FileSystemStorage` class and pass it to the file factory as
    # `storage` argument.
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
**article/models.py**

.. code-block:: python

    from datetime import datetime
    from typing import Optional

    from pydantic import BaseModel, Field

    class User(BaseModel):
        id: int
        username: str = Field(..., max_length=255)
        first_name: str = Field(..., max_length=255)
        last_name: str = Field(..., max_length=255)
        email: str = Field(..., max_length=255)
        password: Optional[str] = Field("", max_length=255)
        last_login: Optional[datetime]
        is_superuser: bool = Field(default=False)
        is_staff: bool = Field(default=False)
        is_active: bool = Field(default=True)
        date_joined: Optional[datetime]

        def __str__(self):
            return self.username

    class Article(BaseModel):
        id: int
        title: str = Field(..., max_length=255)
        slug: str = Field(..., max_length=255, unique=True)
        content: str
        image: Optional[str] = None  # Use str to represent the image path or URL
        pub_date: datetime = Field(default_factory=datetime.now)
        safe_for_work: bool = False
        minutes_to_read: int = 5
        author: User

        def __str__(self):
            return self.title

**article/factories.py**

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

**article/models.py**

.. code-block:: python

    from datetime import datetime

    from tortoise import fields
    from tortoise.models import Model

    class User(Model):

        id = fields.IntField(pk=True)
        username = fields.CharField(max_length=255, unique=True)
        first_name = fields.CharField(max_length=255)
        last_name = fields.CharField(max_length=255)
        email = fields.CharField(max_length=255)
        password = fields.CharField(max_length=255, null=True, blank=True)
        last_login = fields.DatetimeField(null=True, blank=True)
        is_superuser = fields.BooleanField(default=False)
        is_staff = fields.BooleanField(default=False)
        is_active = fields.BooleanField(default=True)
        date_joined = fields.DatetimeField(null=True, blank=True)

        def __str__(self):
            return self.title

    class Article(Model):

        id = fields.IntField(pk=True)
        title = fields.CharField(max_length=255)
        slug = fields.CharField(max_length=255, unique=True)
        content = fields.TextField()
        image = fields.TextField(null=True, blank=True)
        pub_date = fields.DatetimeField(default=datetime.now)
        safe_for_work = fields.BooleanField(default=False)
        minutes_to_read = fields.IntField(default=5)
        author = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)

        def __str__(self):
            return self.title

**article/factories.py**

.. code-block:: python

    from pathlib import Path

    from fake import FACTORY, FileSystemStorage, SubFactory, TortoiseModelFactory

    from article.models import Article, User

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"

    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

    class UserFactory(TortoiseModelFactory):
        """User factory."""

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

**article/models.py**

.. code-block:: python

    from dataclasses import dataclass
    from datetime import datetime
    from typing import Optional

    @dataclass
    class User:
        id: int
        username: str
        first_name: str
        last_name: str
        email: str
        last_login: Optional[datetime]
        date_joined: Optional[datetime]
        password: Optional[str] = None
        is_superuser: bool = False
        is_staff: bool = False
        is_active: bool = True

        def __str__(self):
            return self.username

    @dataclass
    class Article:
        id: int
        title: str
        slug: str
        content: str
        author: User
        image: Optional[str] = None  # Use str to represent the image path or URL
        pub_date: datetime = datetime.now()
        safe_for_work: bool = False
        minutes_to_read: int = 5

        def __str__(self):
            return self.title

**article/factories.py**

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
