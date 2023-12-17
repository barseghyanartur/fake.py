import random
from functools import partial

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.utils import timezone
from fake import (
    FACTORY,
    DjangoModelFactory,
    FileSystemStorage,
    LazyAttribute,
    LazyFunction,
    PostSave,
    PreSave,
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
    "GroupFactory",
    "UserFactory",
)

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


class GroupFactory(DjangoModelFactory):
    """Group factory."""

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
    """User factory.

    Usage example:

    .. code-block:: python

        # Create a user. Created user will automatically have his password
        # set to "test1234" and will be added to the group "Test group".
        user = UserFactory()

        # Create 5 users.
        users = UserFactory.create_batch(5)

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
    """

    username = FACTORY.username()
    first_name = FACTORY.first_name()
    last_name = FACTORY.last_name()
    email = FACTORY.email()
    date_joined = FACTORY.date_time(tzinfo=timezone.get_current_timezone())
    last_login = FACTORY.date_time(tzinfo=timezone.get_current_timezone())
    is_superuser = False
    is_staff = False
    is_active = FACTORY.pybool()
    password = PreSave(set_password, password="test1234")
    group = PostSave(add_to_group, name="TestGroup1234")

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

    @pre_save
    def _pre_save_method(self, instance):
        # For testing purposes only
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        # For testing purposes only
        instance.post_save_called = True


class ArticleFactory(DjangoModelFactory):
    """Article factory.

    Usage example:

    .. code-block:: python

        # Create one article
        article = ArticleFactory()

        # Create 5 articles
        articles = ArticleFactory.create_batch(5)

        # Create one article with authors username set to admin.
        article = ArticleFactory(author__username="admin")
    """

    title = FACTORY.sentence()
    slug = FACTORY.slug()
    content = FACTORY.text()
    headline = LazyAttribute(lambda o: o.content[:25])
    category = LazyFunction(partial(random.choice, CATEGORIES))
    image = FACTORY.png_file(storage=STORAGE)
    pub_date = FACTORY.date(tzinfo=timezone.get_current_timezone())
    safe_for_work = FACTORY.pybool()
    minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
    author = SubFactory(UserFactory)

    class Meta:
        model = Article

    @pre_save
    def _pre_save_method(self, instance):
        # For testing purposes only
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        # For testing purposes only
        instance.post_save_called = True
