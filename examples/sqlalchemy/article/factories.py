from pathlib import Path
from typing import Any, Dict

from fake import (
    FACTORY,
    FAKER,
    FileSystemStorage,
    PostSave,
    PreInit,
    PreSave,
    SQLAlchemyModelFactory,
    SubFactory,
    post_save,
    pre_init,
    pre_save,
    slugify,
    trait,
)

from article.models import Article, Group, User
from config import SESSION

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "ArticleFactory",
    "UserFactory",
)

# Storage config. Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / "media"
STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

CATEGORIES = (
    "art",
    "technology",
    "literature",
)
TAGS = (
    "painting",
    "photography",
    "ai",
    "data-engineering",
    "fiction",
    "poetry",
    "manual",
)


def get_session():
    return SESSION()


class GroupFactory(SQLAlchemyModelFactory):
    """User factory."""

    name = FACTORY.word()

    class Meta:
        model = Group
        get_or_create = ("name",)

    class MetaSQLAlchemy:
        get_session = get_session


def set_password(user: User, password: str) -> None:
    user.set_password(password)


def add_to_group(user: User, name: str) -> None:
    session = get_session()
    # Check if the group already exists
    group = session.query(Group).filter_by(name=name).first()

    # If the group doesn't exist, create a new one
    if not group:
        group = Group(name=name)
        session.add(group)
        session.commit()  # Commit to assign an ID to the new group

    # Add the group to the user's groups using append
    if group not in user.groups:
        user.groups.append(group)
        session.commit()  # Commit the changes


def set_username(data: Dict[str, Any]) -> None:
    first_name = slugify(data["first_name"])
    last_name = slugify(data["last_name"])
    data["username"] = f"{first_name}_{last_name}_{FAKER.pystr().lower()}"


class UserFactory(SQLAlchemyModelFactory):
    """User factory."""

    username = PreInit(set_username)  # type: ignore
    first_name = FACTORY.first_name()  # type: ignore
    last_name = FACTORY.last_name()  # type: ignore
    email = FACTORY.email()  # type: ignore
    date_joined = FACTORY.date_time()  # type: ignore
    last_login = FACTORY.date_time()  # type: ignore
    is_superuser = False
    is_staff = False
    is_active = FACTORY.pybool()  # type: ignore
    password = PreSave(set_password, password="test1234")  # type: ignore
    group = PostSave(add_to_group, name="TestGroup1234")  # type: ignore

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
    def _pre_save_method(self, instance):
        # For testing purposes only
        instance._pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        # For testing purposes only
        instance._post_save_called = True


def set_headline(data: Dict[str, Any]) -> None:
    data["headline"] = data["content"][:25]


class ArticleFactory(SQLAlchemyModelFactory):
    """Article factory."""

    title = FACTORY.sentence()  # type: ignore
    slug = FACTORY.slug()  # type: ignore
    content = FACTORY.text()  # type: ignore
    headline = PreInit(set_headline)
    category = FACTORY.random_choice(elements=CATEGORIES)
    pages = FACTORY.pyint(min_value=1, max_value=100)  # type: ignore
    image = FACTORY.png_file(storage=STORAGE)  # type: ignore
    pub_date = FACTORY.date()  # type: ignore
    safe_for_work = FACTORY.pybool()  # type: ignore
    minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)  # type: ignore
    author = SubFactory(UserFactory)  # type: ignore
    tags = FACTORY.random_sample(elements=TAGS, length=3)

    class Meta:
        model = Article

    class MetaSQLAlchemy:
        get_session = get_session

    @pre_init
    def set_auto_minutes_to_read(self, data: Dict[str, Any]) -> None:
        data["auto_minutes_to_read"] = data["pages"]

    @pre_save
    def _pre_save_method(self, instance):
        # For testing purposes only
        instance._pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        # For testing purposes only
        instance._post_save_called = True
