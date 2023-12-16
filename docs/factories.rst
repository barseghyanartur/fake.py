Factories
=========

- ``pre_save`` a method that will always run before the instance is saved.
- ``post_save`` a method that will always run after the instance is saved.
- ``trait`` decorator runs the code if set to True in factory constructor.
- ``PreSave`` is like the ``pre_save`` decorator of the ``ModelFactory``,
  but you can pass arguments to it and have a lot of flexibility. See
  a working example (below) of how set a user password in Django.
- ``PostSave`` is like the ``post_save`` decorator of the ``ModelFactory``,
  but you can pass arguments to it and have a lot of flexibility. See a
  working example (below) of how to create to assign a user to a Group after
  user creation.
- ``LazyAttribute`` expects a callable, will take the instance, runs it and
  sets the value as an attribute name.
- ``LazyFunction`` expect a callable, runs it and sets the value as
  an attribute name.
- ``SubFactory`` is for specifying relations (typically - ForeignKeys).

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
        headline = models.TextField()
        category = models.CharField()
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

    import random
    from functools import partial

    from django.conf import settings
    from django.contrib.auth.models import Group, User
    from fake import (
        FACTORY,
        DjangoModelFactory,
        FileSystemStorage,
        LazyAttribute,
        LazyFunction,
        SubFactory,
        PreSave,
        PostSave,
        post_save,
        trait,
    )

    from article.models import Article

    # For Django, all files shall be placed inside `MEDIA_ROOT` directory.
    # That's why you need to apply this trick - define a
    # custom `FileSystemStorage` class and pass it to the file factory as
    # `storage` argument.
    STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")
    CATEGORIES = (
        "art",
        "technology",
        "literature",
    )


    class GroupFactory(ModelFactory):
        
        name = FACTORY.word()

        class Meta:
            model = Group
            get_or_create = ("name",)


    def set_password(user: User, password: str) -> None:
        user.set_password(password)


    def add_to_group(user: User, name: str) -> None:
        group = GroupFactory(name=name)
        user.groups.add(group)


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
        password = PreSave(set_password, password="test1234")
        group = PostSave(add_to_group, name="Test group")

        class Meta:
            model = User
            get_or_create = ("username",)

        @post_save
        def _send_registration_email(self, instance):
            """Send an email with registration information."""
            # Your code here

        @trait
        def is_admin_user(self, instance: User) -> None:
            instance.is_superuser = True
            instance.is_staff = True
            instance.is_active = True


    class ArticleFactory(DjangoModelFactory):

        title = FACTORY.sentence()
        slug = FACTORY.slug()
        content = FACTORY.text()
        headline = LazyAttribute(lambda o: o.content[:25])
        category = LazyFunction(partial(random.choice, CATEGORIES))
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

    # Using trait
    user = UserFactory(is_admin_user=True)

    # Using trait in SubFactory
    article = ArticleFactory(author__is_admin_user=True)

    # Create a user. Created user will automatically have his password
    # set to "test1234" and will be added to the group "Test group".
    user = UserFactory()

    # Create a user with custom password
    user = UserFactory(
        password = PreSave(set_password, password="another-pass"),
    )

    # Add a user to another group
    user = UserFactory(
        group = PostSave(add_to_group, name="Another group"),
    )

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
        headline: str
        category: str
        image: Optional[str] = None  # Use str to represent the image path or URL
        pub_date: datetime = Field(default_factory=datetime.now)
        safe_for_work: bool = False
        minutes_to_read: int = 5
        author: User

        def __str__(self):
            return self.title

**article/factories.py**

.. code-block:: python

    import random
    from functools import partial
    from pathlib import Path

    from fake import FACTORY, FileSystemStorage, ModelFactory, SubFactory

    from article.models import Article, User

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"
    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")
    CATEGORIES = (
        "art",
        "technology",
        "literature",
    )

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

        @trait
        def is_admin_user(self, instance: User) -> None:
            instance.is_superuser = True
            instance.is_staff = True
            instance.is_active = True

        @pre_save
        def _set_password(self, instance):
            instance.set_password("test")

    class ArticleFactory(ModelFactory):
        id = FACTORY.pyint()
        title = FACTORY.sentence()
        slug = FACTORY.slug()
        content = FACTORY.text()
        headline = LazyAttribute(lambda o: o.content[:25])
        category = LazyFunction(partial(random.choice, CATEGORIES))
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
        headline = fields.TextField()
        category = fields.CharField(max_length=255)
        image = fields.TextField(null=True, blank=True)
        pub_date = fields.DatetimeField(default=datetime.now)
        safe_for_work = fields.BooleanField(default=False)
        minutes_to_read = fields.IntField(default=5)
        author = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)

        def __str__(self):
            return self.title

**article/factories.py**

.. code-block:: python

    import random
    from functools import partial
    from pathlib import Path

    from fake import FACTORY, FileSystemStorage, SubFactory, TortoiseModelFactory

    from article.models import Article, User

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"
    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")
    CATEGORIES = (
        "art",
        "technology",
        "literature",
    )

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

        @trait
        def is_admin_user(self, instance: User) -> None:
            instance.is_superuser = True
            instance.is_staff = True
            instance.is_active = True

        @pre_save
        def _set_password(self, instance):
            instance.set_password("test")

    class ArticleFactory(TortoiseModelFactory):
        """Article factory."""

        title = FACTORY.sentence()
        slug = FACTORY.slug()
        content = FACTORY.text()
        headline = LazyAttribute(lambda o: o.content[:25])
        category = LazyFunction(partial(random.choice, CATEGORIES))
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

    import random
    from dataclasses import dataclass
    from datetime import datetime
    from functools import partial
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
        headline: str
        category: str
        author: User
        image: Optional[str] = None  # Use str to represent the image path or URL
        pub_date: datetime = datetime.now()
        safe_for_work: bool = False
        minutes_to_read: int = 5

        def __str__(self):
            return self.title

**article/factories.py**

.. code-block:: python

    import random
    from functools import partial
    from pathlib import Path

    from fake import FACTORY, FileSystemStorage, ModelFactory, SubFactory

    from article.models import Article, User

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"
    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")
    CATEGORIES = (
        "art",
        "technology",
        "literature",
    )

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

        @trait
        def is_admin_user(self, instance: User) -> None:
            instance.is_superuser = True
            instance.is_staff = True
            instance.is_active = True

        @pre_save
        def _set_password(self, instance):
            instance.set_password("test")

    class ArticleFactory(ModelFactory):
        id = FACTORY.pyint()
        title = FACTORY.sentence()
        slug = FACTORY.slug()
        content = FACTORY.text()
        headline = LazyAttribute(lambda o: o.content[:25])
        category = LazyFunction(partial(random.choice, CATEGORIES))
        image = FACTORY.png_file(storage=STORAGE)
        pub_date = FACTORY.date()
        safe_for_work = FACTORY.pybool()
        minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
        author = SubFactory(UserFactory)

        class Meta:
            model = Article

*Used just like in previous example.*

SQLAlchemy example
------------------

**config.py**

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    DATABASE_URL = "sqlite:///test_database.db"
    ENGINE = create_engine(DATABASE_URL)
    SESSION = scoped_session(sessionmaker(bind=ENGINE))

**article/models.py**

.. code-block:: python

    from datetime import datetime

    from sqlalchemy import (
        Boolean,
        Column,
        DateTime,
        ForeignKey,
        Integer,
        String,
        Text,
    )
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class User(Base):
        """User model."""

        __tablename__ = "users"

        id = Column(Integer, primary_key=True)
        username = Column(String(255), unique=True)
        first_name = Column(String(255))
        last_name = Column(String(255))
        email = Column(String(255))
        password = Column(String(255), nullable=True)
        last_login = Column(DateTime, nullable=True)
        is_superuser = Column(Boolean, default=False)
        is_staff = Column(Boolean, default=False)
        is_active = Column(Boolean, default=True)
        date_joined = Column(DateTime, nullable=True)

        articles = relationship("Article", back_populates="author")

    class Article(Base):
        """Article model."""

        __tablename__ = "articles"

        id = Column(Integer, primary_key=True)
        title = Column(String(255))
        slug = Column(String(255), unique=True)
        content = Column(Text)
        headline = Column(Text)
        category = Column(String(255))
        image = Column(Text, nullable=True)
        pub_date = Column(DateTime, default=datetime.utcnow)
        safe_for_work = Column(Boolean, default=False)
        minutes_to_read = Column(Integer, default=5)
        author_id = Column(Integer, ForeignKey("users.id"))

        author = relationship("User", back_populates="articles")

**article/factories.py**

Pay attention to the ``MetaSQLAlchemy`` meta-class and the ``get_session`` 
method.

.. code-block:: python

    import random
    from functools import partial
    from pathlib import Path

    from fake import (
        FACTORY,
        FileSystemStorage,
        SQLAlchemyModelFactory,
        SubFactory,
        post_save,
        pre_save,
        trait,
    )

    from article.models import Article, User
    from config import SESSION

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = BASE_DIR / "media"
    STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")
    CATEGORIES = (
        "art",
        "technology",
        "literature",
    )

    def get_session():
        return SESSION()

    class UserFactory(SQLAlchemyModelFactory):
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

        class MetaSQLAlchemy:
            get_session = get_session

        @trait
        def is_admin_user(self, instance: User) -> None:
            instance.is_superuser = True
            instance.is_staff = True
            instance.is_active = True

        @pre_save
        def _set_password(self, instance):
            instance.set_password("test")

    class ArticleFactory(SQLAlchemyModelFactory):
        """Article factory."""

        title = FACTORY.sentence()
        slug = FACTORY.slug()
        content = FACTORY.text()
        headline = LazyAttribute(lambda o: o.content[:25])
        category = LazyFunction(partial(random.choice, CATEGORIES))
        image = FACTORY.png_file(storage=STORAGE)
        pub_date = FACTORY.date()
        safe_for_work = FACTORY.pybool()
        minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
        author = SubFactory(UserFactory)

        class Meta:
            model = Article

        class MetaSQLAlchemy:
            get_session = get_session

*Used just like in previous example.*
