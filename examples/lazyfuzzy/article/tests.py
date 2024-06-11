import unittest
from datetime import datetime

from fake import FILE_REGISTRY

from article.factories import ArticleFactory
from article.models import Article, User

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("FactoriesTestCase",)


class FactoriesTestCase(unittest.TestCase):
    def tearDown(self):
        FILE_REGISTRY.clean_up()

    def test_sub_factory(self) -> None:
        article = ArticleFactory()

        # Testing SubFactory
        self.assertIsInstance(article.author, User)
        self.assertIsInstance(article.author.id, int)  # type: ignore
        self.assertIsInstance(article.author.is_staff, bool)  # type: ignore
        self.assertIsInstance(
            article.author.date_joined,  # type: ignore
            datetime,
        )

        # Testing Factory
        self.assertIsInstance(article.id, int)
        self.assertIsInstance(article.slug, str)

        # Testing hooks
        self.assertTrue(
            hasattr(article, "_pre_save_called") and article._pre_save_called
        )
        self.assertTrue(
            hasattr(article, "_post_save_called") and article._post_save_called
        )
        self.assertTrue(
            hasattr(article.author, "_pre_save_called")
            and article.author._pre_save_called
        )
        self.assertTrue(
            hasattr(article.author, "_post_save_called")
            and article.author._post_save_called
        )

        # Testing batch creation
        articles = ArticleFactory.create_batch(5)
        self.assertEqual(len(articles), 5)
        self.assertIsInstance(articles[0], Article)
