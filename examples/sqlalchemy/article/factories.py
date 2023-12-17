from pathlib import Path

from fake import (
    FACTORY,
    FileSystemStorage,
    PostSave,
    PreSave,
    SQLAlchemyModelFactory,
    SubFactory,
    post_save,
    pre_save,
    trait,
)

from article.models import Article, Group, User
from config import SESSION

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "ArticleFactory",
    "UserFactory",
)

# Storage config. Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / "media"
STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")


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


class UserFactory(SQLAlchemyModelFactory):
    """User factory."""

    username = FACTORY.username()  # mypy: ignore
    first_name = FACTORY.first_name()  # mypy: ignore
    last_name = FACTORY.last_name()  # mypy: ignore
    email = FACTORY.email()  # mypy: ignore
    date_joined = FACTORY.date_time()  # mypy: ignore
    last_login = FACTORY.date_time()  # mypy: ignore
    is_superuser = False
    is_staff = False
    is_active = FACTORY.pybool()  # mypy: ignore
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
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        # For testing purposes only
        instance.post_save_called = True


class ArticleFactory(SQLAlchemyModelFactory):
    """Article factory."""

    title = FACTORY.sentence()  # mypy: ignore
    slug = FACTORY.slug()  # mypy: ignore
    content = FACTORY.text()  # mypy: ignore
    image = FACTORY.png_file(storage=STORAGE)  # mypy: ignore
    pub_date = FACTORY.date()  # mypy: ignore
    safe_for_work = FACTORY.pybool()  # mypy: ignore
    minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)  # mypy: ignore
    author = SubFactory(UserFactory)  # mypy: ignore

    class Meta:
        model = Article

    class MetaSQLAlchemy:
        get_session = get_session

    @pre_save
    def _pre_save_method(self, instance):
        # For testing purposes only
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        # For testing purposes only
        instance.post_save_called = True
