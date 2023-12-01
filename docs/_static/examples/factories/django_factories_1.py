from django.conf import settings
from django.contrib.auth.models import User
from fake import (
    DjangoModelFactory,
    Factory,
    FileSystemStorage,
    SubFactory,
    pre_save,
)

from article.models import Article

STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")


class UserFactory(DjangoModelFactory):
    username = Factory.username()
    first_name = Factory.first_name()
    last_name = Factory.last_name()
    email = Factory.email()
    last_login = Factory.date_time()
    is_superuser = False
    is_staff = False
    is_active = Factory.pybool()
    date_joined = Factory.date_time()

    class Meta:
        model = User

    @pre_save
    def __set_password(instance):
        instance.set_password("test")


class ArticleFactory(DjangoModelFactory):
    title = Factory.sentence()
    slug = Factory.slug()
    content = Factory.text()
    image = Factory.png_file(storage=STORAGE)
    pub_date = Factory.date()
    safe_for_work = Factory.pybool()
    minutes_to_read = Factory.pyint(min_value=1, max_value=10)
    author = SubFactory(UserFactory)

    class Meta:
        model = Article
