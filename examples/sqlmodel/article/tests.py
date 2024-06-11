import unittest

from fake import xor_transform

from article.factories import ArticleFactory, UserFactory
from config import SESSION

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("TestFactories",)


class TestFactories(unittest.TestCase):
    def setUp(self):
        # Set up database session, if needed
        self.session = SESSION()

    def tearDown(self):
        # Clean up the session after each test
        self.session.rollback()
        self.session.close()

    def test_user_creation(self):
        user = UserFactory(username="testuser")
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "testuser")

    def test_article_creation(self):
        user = UserFactory(username="authoruser")
        article = ArticleFactory(title="Test Article", author=user)
        self.assertIsNotNone(article.id)
        self.assertEqual(article.author.username, "authoruser")

    def test_pre_save_and_post_save(self) -> None:
        """Test PreSave and PostSave."""
        user = UserFactory(is_staff=True)
        self.assertEqual(
            xor_transform(user.password),
            "test1234",
        )
        self.assertEqual(list(user.groups)[0].name, "TestGroup1234")
