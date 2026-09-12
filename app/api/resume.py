import os

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.resume import Resume
from app.models.user import User
from app.services.resume_service import extract_text_from_pdf


router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    # Use the actual user ID
    current_user_id = current_user.id

    # Create safe file path
    file_path = os.path.join(
        UPLOAD_DIR,
        f"{current_user_id}_{file.filename}",
    )

    # Read uploaded file
    contents = await file.read()

    # Save PDF
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(file_path)

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from resume",
        )

    # Save resume in database
    resume = Resume(
        user_id=current_user_id,
        filename=file.filename,
        file_path=file_path,
        extracted_text=resume_text,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "filename": resume.filename,
        "user_id": current_user_id,
        "text_preview": resume.extracted_text[:500],
    }