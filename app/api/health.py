from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["health"])

PROJECT_NAME = "HireSense AI API"
PROJECT_VERSION = "1.0.0"


@router.get("/", summary="Health check", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "project_name": PROJECT_NAME,
        "version": PROJECT_VERSION,
    }
