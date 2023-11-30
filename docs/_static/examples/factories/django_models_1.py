from django.conf import settings
from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    pub_date = models.DateTimeField(default=timezone.now)
    safe_for_work = models.BooleanField(default=False)
    minutes_to_read = models.IntegerField(default=5)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
