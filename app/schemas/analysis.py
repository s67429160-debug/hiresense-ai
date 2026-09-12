from pydantic import BaseModel, Field


class JobDescriptionInput(BaseModel):
    job_description: str = Field(
        ...,
        min_length=20,
        description="Job description to compare with the resume"
    )