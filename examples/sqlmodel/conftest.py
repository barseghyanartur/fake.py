import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables once before any tests run."""
    from config import create_tables  # noqa
    from article.models import Article, Group, User  # noqa

    create_tables()
