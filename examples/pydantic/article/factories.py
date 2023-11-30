from fake import Factory, ModelFactory

from article.models import Article


class ArticleFactory(ModelFactory):
    title = Factory.sentence()
    slug = Factory.slug()
    content = Factory.text()
    # image = Factory.png_file(storage=STORAGE)
    pub_date = Factory.date()
    safe_for_work = Factory.pybool()
    minutes_to_read = Factory.pyint(min_value=1, max_value=10)
    # author = SubFactory(UserFactory)

    class Meta:
        model = Article
