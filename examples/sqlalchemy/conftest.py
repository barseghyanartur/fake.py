import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables before any tests run, and drop them when the
    session ends.
    """
    from article.models import Base
    from config import ENGINE

    Base.metadata.create_all(ENGINE)
    yield
    Base.metadata.drop_all(ENGINE)


@pytest.fixture(scope="function")
def db_session():
    """Provide a new database session for a test and roll back after each
    test.
    """
    from sqlalchemy.orm import sessionmaker

    from config import ENGINE

    # Establish a connection and start a transaction
    connection = ENGINE.connect()
    transaction = connection.begin()

    # Bind a sessionmaker to the connection
    session_cls = sessionmaker(bind=connection)
    session = session_cls()

    try:
        yield session
    finally:
        # Roll back any changes and close resources
        session.close()
        transaction.rollback()
        connection.close()
