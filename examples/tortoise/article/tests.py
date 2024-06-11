from datetime import datetime

from fake import FILE_REGISTRY, run_async_in_thread, xor_transform
from tortoise.contrib import test
from tortoise.contrib.test import finalizer, initializer

from article.factories import ArticleFactory, UserFactory
from article.models import Article, User

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("FactoriesTestCase",)


class FactoriesTestCase(test.TestCase):
    @classmethod
    def setUpClass(cls):
        initializer(["article.models"], db_url="sqlite://:memory:")
        # Your setup code...

    @classmethod
    def tearDownClass(cls):
        finalizer()
        # Your teardown code...

    def tearDown(self):
        FILE_REGISTRY.clean_up()

    def test_sub_factory(self) -> None:
        with self.subTest("SubFactory"):
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
                hasattr(article, "_pre_save_called")
                and article._pre_save_called
            )
            self.assertTrue(
                hasattr(article, "_post_save_called")
                and article._post_save_called
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

        with self.subTest("SubFactory nested params"):
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
                hasattr(article, "_pre_save_called")
                and article._pre_save_called
            )
            self.assertTrue(
                hasattr(article, "_post_save_called")
                and article._post_save_called
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
        self.assertEqual(
            xor_transform(user.password),
            "test1234",
        )

        async def get_first_group_name():
            first_group = await user.groups.all().first()
            if first_group:
                return first_group.name
            return None

        group_name = run_async_in_thread(get_first_group_name())
        self.assertEqual(group_name, "TestGroup1234")
