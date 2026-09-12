from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.core.dependencies import get_current_user
from app.database.database import get_db

from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import Analysis

from app.schemas.analysis import JobDescriptionInput

from app.services.ats_service import calculate_ats_score
from app.services.recommendation_service import generate_recommendations


def generate_ats_report(
    analysis,
    resume_filename,
    user_name,
    matched_skills,
    missing_skills,
    score_breakdown,
    recommendations,
):
    """Generate the ATS report locally so this router has no missing import."""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen.canvas import Canvas
    from tempfile import NamedTemporaryFile

    report = NamedTemporaryFile(
        prefix=f"HireSense_ATS_Report_{analysis.id}_",
        suffix=".pdf",
        delete=False,
    )
    report.close()
    canvas = Canvas(report.name, pagesize=letter)
    width, height = letter
    y = height - 50

    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(50, y, "HireSense ATS Report")
    y -= 35
    canvas.setFont("Helvetica", 11)
    for label, value in (
        ("Candidate", user_name),
        ("Resume", resume_filename),
        ("ATS Score", getattr(analysis, "ats_score", "N/A")),
    ):
        canvas.drawString(50, y, f"{label}: {value}")
        y -= 18

    sections = (
        ("Matched Skills", matched_skills),
        ("Missing Skills", missing_skills),
        ("Recommendations", recommendations),
        ("Score Breakdown", score_breakdown),
    )
    for title, values in sections:
        y -= 12
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(50, y, title)
        y -= 17
        canvas.setFont("Helvetica", 10)
        items = values.items() if isinstance(values, dict) else values
        for item in items or []:
            text = f"{item[0]}: {item[1]}" if isinstance(item, tuple) else str(item)
            canvas.drawString(65, y, text[:105])
            y -= 14
            if y < 50:
                canvas.showPage()
                y = height - 50
                canvas.setFont("Helvetica", 10)
    canvas.save()
    return report.name


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


# =========================================================
# ANALYZE RESUME
# =========================================================

@router.post("/")
def analyze_resume(
    data: JobDescriptionInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    resume = (
        db.query(Resume)
        .filter(
            Resume.user_id == current_user.id
        )
        .order_by(
            Resume.created_at.desc()
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="No resume found. Please upload a resume first."
        )

    # Calculate ATS score
    result = calculate_ats_score(
        resume_text=resume.extracted_text,
        job_description=data.job_description
    )

    # Generate recommendations
    recommendations = generate_recommendations(
        result["missing_skills"]
    )

    # Save analysis
    analysis = Analysis(
        user_id=current_user.id,
        resume_id=resume.id,
        job_description=data.job_description,
        ats_score=result["ats_score"],
        matched_skills=",".join(
            result["matched_skills"]
        ),
        missing_skills=",".join(
            result["missing_skills"]
        )
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return {
        "user_id": current_user.id,
        "analysis_id": analysis.id,
        "resume_id": resume.id,
        "filename": resume.filename,
        "message": "Resume analysis completed",
        **result,
        "recommendations": recommendations
    }


# =========================================================
# ANALYSIS HISTORY
# =========================================================

@router.get("/history")
def get_analysis_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    analyses = (
        db.query(Analysis)
        .filter(
            Analysis.user_id == current_user.id
        )
        .order_by(
            Analysis.created_at.desc()
        )
        .all()
    )

    history = []

    for analysis in analyses:

        history.append({
            "analysis_id": analysis.id,

            "resume_id": analysis.resume_id,

            "ats_score": analysis.ats_score,

            "job_description": analysis.job_description,

            "matched_skills": (
                analysis.matched_skills.split(",")
                if analysis.matched_skills
                else []
            ),

            "missing_skills": (
                analysis.missing_skills.split(",")
                if analysis.missing_skills
                else []
            ),

            "created_at": analysis.created_at
        })

    return {
        "user_id": current_user.id,
        "total_analyses": len(history),
        "history": history
    }


# =========================================================
# DOWNLOAD ATS REPORT
# =========================================================

@router.get("/{analysis_id}/report")
def download_analysis_report(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # -----------------------------------------------------
    # Find analysis
    # -----------------------------------------------------

    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.id == analysis_id,
            Analysis.user_id == current_user.id
        )
        .first()
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )


    # -----------------------------------------------------
    # Find resume
    # -----------------------------------------------------

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == analysis.resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )


    # -----------------------------------------------------
    # Get matched skills
    # -----------------------------------------------------

    matched_skills = (
        analysis.matched_skills.split(",")
        if analysis.matched_skills
        else []
    )


    # -----------------------------------------------------
    # Get missing skills
    # -----------------------------------------------------

    missing_skills = (
        analysis.missing_skills.split(",")
        if analysis.missing_skills
        else []
    )


    # -----------------------------------------------------
    # Recalculate ATS result
    # -----------------------------------------------------

    result = calculate_ats_score(
        resume_text=resume.extracted_text,
        job_description=analysis.job_description
    )


    # -----------------------------------------------------
    # Generate recommendations
    # -----------------------------------------------------

    recommendations = generate_recommendations(
        result["missing_skills"]
    )


    # -----------------------------------------------------
    # Generate PDF
    # -----------------------------------------------------

    try:

        file_path = generate_ats_report(
            analysis=analysis,
            resume_filename=resume.filename,
            user_name=current_user.full_name,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            score_breakdown=result["score_breakdown"],
            recommendations=recommendations
        )

    except Exception as e:

        print("PDF GENERATION ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=f"Could not generate ATS report: {str(e)}"
        )


    # -----------------------------------------------------
    # Verify PDF exists
    # -----------------------------------------------------

    if not file_path:
        raise HTTPException(
            status_code=500,
            detail="PDF report path is empty."
        )


    absolute_path = os.path.abspath(file_path)

    print("PDF PATH:", absolute_path)


    if not os.path.isfile(absolute_path):

        raise HTTPException(
            status_code=500,
            detail=f"ATS report file not found: {absolute_path}"
        )


    # -----------------------------------------------------
    # Return PDF
    # -----------------------------------------------------

    return FileResponse(
        path=absolute_path,
        media_type="application/pdf",
        filename=f"HireSense_ATS_Report_{analysis.id}.pdf"
    )