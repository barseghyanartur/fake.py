from django.contrib import admin

from article.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "minutes_to_read",
        "safe_for_work",
        "pub_date",
    )
    list_filter = ("safe_for_work",)
