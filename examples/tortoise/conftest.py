import pytest


async def init():
    # Initialise SQLite DB and specify the app name of "models"
    #  alongside the models "article.models"
    from tortoise import Tortoise

    await Tortoise.init(
        db_url="sqlite://:memory:",
        # db_url="sqlite://tortoise_db.sqlite3",
        modules={"models": ["article.models"]},
    )
    # Generate the schema
    await Tortoise.generate_schemas()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables once before any tests run."""
    from tortoise import run_async

    run_async(init())
