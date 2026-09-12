from app.api.profile import router as profile_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.analysis import router as analysis_router

from app.database.base import Base
from app.database.database import engine

from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import Analysis


def create_app() -> FastAPI:
    app = FastAPI(
        title="HireSense AI API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(health_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(resume_router, prefix="/api/v1")
    app.include_router(analysis_router, prefix="/api/v1")
    app.include_router(profile_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {"message": "Welcome to HireSense AI API"}

    return app


app = create_app()