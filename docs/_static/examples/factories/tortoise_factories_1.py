from pathlib import Path

from fake import Factory, FileSystemStorage, SubFactory, TortoiseModelFactory

from article.models import Article, User

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / "media"

STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")


class UserFactory(TortoiseModelFactory):
    id = Factory.pyint()
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


class ArticleFactory(TortoiseModelFactory):
    id = Factory.pyint()
    title = Factory.sentence()
    slug = Factory.slug()
    content = Factory.text()
    image = Factory.png_file(storage=STORAGE)
    pub_date = Factory.date_time()
    safe_for_work = Factory.pybool()
    minutes_to_read = Factory.pyint(min_value=1, max_value=10)
    author = SubFactory(UserFactory)

    class Meta:
        model = Article
