from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import Analysis

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    latest_resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .first()
    )

    analyses = (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.created_at.desc())
        .all()
    )

    return {
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "created_at": current_user.created_at,
        },
        "latest_resume": (
            {
                "id": latest_resume.id,
                "filename": latest_resume.filename,
                "created_at": latest_resume.created_at,
            }
            if latest_resume
            else None
        ),
        "analysis_stats": {
            "total_analyses": len(analyses),
            "latest_ats_score": (
                analyses[0].ats_score
                if analyses
                else None
            ),
            "highest_ats_score": (
                max(a.ats_score for a in analyses)
                if analyses
                else None
            ),
        },
    }