from sqlalchemy.orm import declarative_base 

# Base class for SQLAlchemy models.
# Models should inherit from this `Base` to be registered with SQLAlchemy's ORM.
Base = declarative_base()
