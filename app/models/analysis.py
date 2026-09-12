from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func

from app.database.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False,
    )

    job_description = Column(
        Text,
        nullable=False,
    )

    ats_score = Column(
        Integer,
        nullable=False,
    )

    matched_skills = Column(
        Text,
        nullable=False,
    )

    missing_skills = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )