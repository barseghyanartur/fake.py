from pathlib import Path

from fake import (
    FACTORY,
    FileSystemStorage,
    ModelFactory,
    PostSave,
    PreSave,
    SubFactory,
    post_save,
    pre_save,
    trait,
)

from article.models import Article, Group, User

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "ArticleFactory",
    "GroupFactory",
    "UserFactory",
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / "media"

STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")


class GroupFactory(ModelFactory):
    id = FACTORY.pyint()
    name = FACTORY.word()

    class Meta:
        model = Group
        get_or_create = ("name",)


def set_password(user: User, password: str) -> None:
    user.set_password(password)


def add_to_group(user: User, name: str) -> None:
    group = GroupFactory(name=name)
    user.groups.add(group)


class UserFactory(ModelFactory):
    id = FACTORY.pyint()
    username = FACTORY.username()
    first_name = FACTORY.first_name()
    last_name = FACTORY.last_name()
    email = FACTORY.email()
    date_joined = FACTORY.date_time()
    last_login = FACTORY.date_time()
    is_superuser = False
    is_staff = False
    is_active = FACTORY.pybool()
    password = PreSave(set_password, password="test1234")  # type: ignore
    group = PostSave(add_to_group, name="TestGroup1234")  # type: ignore

    class Meta:
        model = User

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

    @pre_save
    def _pre_save_method(self, instance):
        # For testing purposes only
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        # For testing purposes only
        instance.post_save_called = True
