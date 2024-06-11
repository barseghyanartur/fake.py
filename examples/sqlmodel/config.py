from sqlalchemy.orm import scoped_session, sessionmaker
from sqlmodel import SQLModel, create_engine

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "DATABASE_URL",
    "ENGINE",
    "SESSION",
)

# SQLAlchemy
DATABASE_URL = "sqlite:///test_database.db"
ENGINE = create_engine(DATABASE_URL)
SESSION = scoped_session(sessionmaker(bind=ENGINE))


def create_tables():
    """Create tables."""
    SQLModel.metadata.create_all(ENGINE)


def get_db():
    """Get database connection."""
    session = SESSION()
    try:
        yield session
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    create_tables()
