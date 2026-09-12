from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.models.user import User
from app.models.resume import Resume


# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./hiresense.db"


# Create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
