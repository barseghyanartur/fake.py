from pathlib import Path

from fake import (
    FACTORY,
    FileSystemStorage,
    ModelFactory,
    SubFactory,
    post_save,
    pre_save,
    trait,
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
    def _pre_save_method(self, instance):
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
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
        instance.pre_save_called = True

    @post_save
    def _post_save_method(self, instance):
        instance.post_save_called = True
