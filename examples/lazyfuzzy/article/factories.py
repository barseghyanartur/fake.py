import random
from datetime import datetime
from functools import partial
from pathlib import Path

from fake import (
    FACTORY,
    FileSystemStorage,
    LazyAttribute,
    LazyFunction,
    ModelFactory,
    SubFactory,
    post_save,
    pre_save,
    trait,
)

from article.models import Article, User

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "ArticleFactory",
    "UserFactory",
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / "media"

STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")
CATEGORIES = (
    "art",
    "technology",
    "literature",
)


class UserFactory(ModelFactory):
    id = FACTORY.pyint()  # type: ignore
    username = FACTORY.username()  # type: ignore
    first_name = FACTORY.first_name()  # type: ignore
    last_name = FACTORY.last_name()  # type: ignore
    email = LazyAttribute(lambda o: f"{o.username}@example.com")
    last_login = FACTORY.date_time()  # type: ignore
    is_superuser = False
    is_staff = False
    is_active = FACTORY.pybool()  # type: ignore
    date_joined = LazyFunction(datetime.now)

    class Meta:
        model = User

    @trait
    def is_admin_user(self, instance: User) -> None:
        instance.is_superuser = True
        instance.is_staff = True
        instance.is_active = True

    @pre_save
    def _pre_save_method(self, instance):
        instance._pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        instance._post_save_called = True


class ArticleFactory(ModelFactory):
    id = FACTORY.pyint()  # type: ignore
    title = FACTORY.sentence()  # type: ignore
    slug = FACTORY.slug()  # type: ignore
    content = FACTORY.text()  # type: ignore
    headline = LazyAttribute(lambda o: o.content[:25])
    category = LazyFunction(partial(random.choice, CATEGORIES))
    image = FACTORY.png_file(storage=STORAGE)  # type: ignore
    pub_date = FACTORY.date()  # type: ignore
    safe_for_work = FACTORY.pybool()  # type: ignore
    minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)  # type: ignore
    author = SubFactory(UserFactory)

    class Meta:
        model = Article

    @pre_save
    def _pre_save_method(self, instance):
        instance._pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        instance._post_save_called = True
