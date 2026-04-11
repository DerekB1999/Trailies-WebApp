import os

from sqlmodel import Session, create_engine

# Tries to read the DATABASE_URL from environment
DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql://postgres:password@db:5432/appdb'
)

# This engine gets reused across the app
# echo=False so there's no SQL logging, would be true in production
engine = create_engine(DATABASE_URL, echo=False)

# Used by FastAPI dependency injection, providing database session per request


def get_session():
    with Session(engine) as session:
        yield session
