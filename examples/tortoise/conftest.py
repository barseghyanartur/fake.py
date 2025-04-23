import asyncio

import pytest
import pytest_asyncio
from tortoise import Tortoise


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an instance of the default event loop for session-scoped
    async fixtures.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_db():
    """
    Initialize Tortoise ORM with an in-memory SQLite database and generate
    schemas before tests, then close connections (dropping the in-memory DB)
    after.
    """
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["article.models"]},
    )
    await Tortoise.generate_schemas()
    yield
    # Teardown: close connections to drop the in-memory database
    await Tortoise.close_connections()
