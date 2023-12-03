from datetime import datetime

from tortoise import fields
from tortoise.models import Model

__all__ = (
    "Article",
    "User",
)


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

    def __str__(self):
        return self.title


class Article(Model):
    """Article model."""

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255, unique=True)
    content = fields.TextField()
    image = fields.TextField(null=True, blank=True)
    pub_date = fields.DatetimeField(default=datetime.now)
    safe_for_work = fields.BooleanField(default=False)
    minutes_to_read = fields.IntField(default=5)
    author = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)

    def __str__(self):
        return self.title
