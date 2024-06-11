from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from fake import FILE_REGISTRY

from article.factories import ArticleFactory, GroupFactory, UserFactory
from article.models import Article

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("FactoriesTestCase",)


class FactoriesTestCase(TestCase):
    def tearDown(self):
        super().tearDown()
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

    def test_sub_factory_nested(self) -> None:
        article = ArticleFactory(author__username="admin")

        # Testing SubFactory
        self.assertIsInstance(article.author, User)
        self.assertIsInstance(article.author.id, int)
        self.assertIsInstance(article.author.is_staff, bool)
        self.assertIsInstance(article.author.date_joined, datetime)
        self.assertEqual(article.author.username, "admin")

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

    def test_pre_save_and_post_save(self) -> None:
        """Test PreSave and PostSave."""
        user = UserFactory(is_staff=True, is_active=True)
        self.assertTrue(
            self.client.login(
                username=user.username,
                password="test1234",
            )
        )
        self.assertTrue(user.groups.first().name == "TestGroup1234")

    def test_group_factory(self):
        group = GroupFactory()
        assert group.name

    def test_user_factory(self):
        user = UserFactory()
        assert user.id

    def test_article_factory(self):
        article = ArticleFactory()
        assert article.id
