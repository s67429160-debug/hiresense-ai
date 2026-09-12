from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func

from app.database.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    filename = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    extracted_text = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )