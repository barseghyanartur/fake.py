from pathlib import Path

from fake import (
    FACTORY,
    FileSystemStorage,
    SubFactory,
    TortoiseModelFactory,
    post_save,
    pre_save,
)

from article.models import Article, User

__all__ = (
    "ArticleFactory",
    "UserFactory",
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
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

    @staticmethod
    @pre_save
    def __pre_save_method(instance):
        instance.pre_save_called = True

    @staticmethod
    @post_save
    def __post_save_method(instance):
        instance.post_save_called = True


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

    @staticmethod
    @pre_save
    def __pre_save_method(instance):
        instance.pre_save_called = True

    @staticmethod
    @post_save
    def __post_save_method(instance):
        instance.post_save_called = True
