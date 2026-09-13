import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import Analysis


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./hiresense.db"
)

# Render PostgreSQL may provide a postgres:// URL.
# SQLAlchemy requires postgresql://.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

if DATABASE_URL.startswith("postgresql://"):
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        