from django.conf import settings
from django.db import models
from django.utils import timezone

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("Article",)


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    headline = models.TextField()
    category = models.CharField(max_length=255)
    pages = models.IntegerField()
    auto_minutes_to_read = models.IntegerField()
    image = models.ImageField(null=True, blank=True)
    pub_date = models.DateField(default=timezone.now)
    safe_for_work = models.BooleanField(default=False)
    minutes_to_read = models.IntegerField(default=5)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    tags = models.JSONField(default=list)

    def __str__(self):
        return self.title
