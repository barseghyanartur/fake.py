from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from fake import (
    FACTORY,
    DjangoModelFactory,
    FileSystemStorage,
    SubFactory,
    post_save,
    pre_save,
    trait,
)

from article.models import Article

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "ArticleFactory",
    "UserFactory",
)

STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")


class UserFactory(DjangoModelFactory):
    """User factory.

    Usage example:

    .. code-block:: python

        user = UserFactory()
        users = UserFactory.create_batch(5)
    """

    username = FACTORY.username()
    first_name = FACTORY.first_name()
    last_name = FACTORY.last_name()
    email = FACTORY.email()
    last_login = FACTORY.date_time(tzinfo=timezone.get_current_timezone())
    is_superuser = False
    is_staff = False
    is_active = FACTORY.pybool()
    date_joined = FACTORY.date_time(tzinfo=timezone.get_current_timezone())

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

    @pre_save
    def _pre_save_method(self, instance):
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        instance.post_save_called = True


class ArticleFactory(DjangoModelFactory):
    """Article factory.

    Usage example:

        article = ArticleFactory()
        articles = ArticleFactory.create_batch(5)
    """

    title = FACTORY.sentence()
    slug = FACTORY.slug()
    content = FACTORY.text()
    image = FACTORY.png_file(storage=STORAGE)
    pub_date = FACTORY.date(tzinfo=timezone.get_current_timezone())
    safe_for_work = FACTORY.pybool()
    minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
    author = SubFactory(UserFactory)

    class Meta:
        model = Article

    @pre_save
    def _pre_save_method(self, instance):
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        instance.post_save_called = True
