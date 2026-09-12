from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserRegister

class UserService:
    @staticmethod
    def create_user(db: Session, user_in: UserRegister) -> User:
        """Create a new user record in the database.

        Important: do not hash the password yet. Store the raw password value
        in `hashed_password` for now until password hashing is implemented.
        """
        # Create a User instance from the incoming schema.
        user = User(
            full_name=user_in.full_name,
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
        )

        # Add the new user to the current database session.
        db.add(user)

        # Commit the transaction to persist the user in the database.
        db.commit()

        # Refresh the instance to load any database-generated fields.
        db.refresh(user)

        # Return the persisted User object.
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Query the database for a user by email."""
        return db.query(User).filter(User.email == email).first()
