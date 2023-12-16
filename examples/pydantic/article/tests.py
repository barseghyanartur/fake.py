import unittest
from datetime import datetime

from fake import FILE_REGISTRY, xor_transform

from article.factories import ArticleFactory, UserFactory
from article.models import Article, User

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("FactoriesTestCase",)


class FactoriesTestCase(unittest.TestCase):
    def tearDown(self):
        FILE_REGISTRY.clean_up()

    def test_sub_factory(self) -> None:
        article = ArticleFactory()

        # Testing SubFactory
        self.assertIsInstance(article.author, User)
        self.assertIsInstance(article.author.id, int)
        self.assertIsInstance(article.author.is_staff, bool)
        self.assertIsInstance(article.author.date_joined, datetime)

        # Testing Factory
        self.assertIsInstance(article.id, int)
        self.assertIsInstance(article.slug, str)

        # Testing hooks
        self.assertTrue(
            hasattr(article, "pre_save_called") and article.pre_save_called
        )
        self.assertTrue(
            hasattr(article, "post_save_called") and article.post_save_called
        )
        self.assertTrue(
            hasattr(article.author, "pre_save_called")
            and article.author.pre_save_called
        )
        self.assertTrue(
            hasattr(article.author, "post_save_called")
            and article.author.post_save_called
        )

        # Testing batch creation
        articles = ArticleFactory.create_batch(5)
        self.assertEqual(len(articles), 5)
        self.assertIsInstance(articles[0], Article)

    def test_pre_save_and_post_save(self) -> None:
        """Test PreSave and PostSave."""
        user = UserFactory(is_staff=True)
        self.assertEqual(
            xor_transform(user.password),
            "test1234",
        )
        self.assertEqual(list(user.groups)[0].name, "TestGroup1234")
