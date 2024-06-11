from datetime import date

from fake import xor_transform
from tortoise import fields
from tortoise.models import Model

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "Article",
    "Group",
    "User",
)


class Group(Model):
    """Group model."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(Model):
    """User model."""

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255, null=True, blank=True)
    last_login = fields.DatetimeField(null=True, blank=True)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    date_joined = fields.DatetimeField(null=True, blank=True)
    groups = fields.ManyToManyField("models.Group", on_delete=fields.CASCADE)

    def __str__(self):
        return self.title

    def set_password(self, password: str) -> None:
        self.password = xor_transform(password)


class Article(Model):
    """Article model."""

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255, unique=True)
    content = fields.TextField()
    headline = fields.TextField()
    category = fields.CharField(max_length=255)
    pages = fields.IntField()
    auto_minutes_to_read = fields.IntField()
    image = fields.TextField(null=True, blank=True)
    pub_date = fields.DateField(default=date.today)
    safe_for_work = fields.BooleanField(default=False)
    minutes_to_read = fields.IntField(default=5)
    author = fields.ForeignKeyField(
        "models.User",
        on_delete=fields.CASCADE,
    )
    tags = fields.JSONField(default=list)

    def __str__(self):
        return self.title
