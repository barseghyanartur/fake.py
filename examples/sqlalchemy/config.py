from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
