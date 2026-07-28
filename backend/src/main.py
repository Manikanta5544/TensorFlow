import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from src.ai.api.router import router as ai_router
from src.applications.api.router import router as applications_router
from src.auth.api.router import router as auth_router
from src.jobs.api.router import router as jobs_router
from src.shared.config.settings import get_settings
from src.shared.database.session import SessionLocal
from src.shared.exceptions.exceptions import AppError
from src.shared.logging.logging_config import configure_logging
from src.shared.middleware.request_logging import RequestContextMiddleware
from src.shared.responses.envelope import fail

settings = get_settings()
configure_logging(settings.LOG_LEVEL)
logger = logging.getLogger("tensorflow.main")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        return JSONResponse(status_code=exc.http_status, content=fail(exc.code, exc.message))

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        safe_errors = jsonable_encoder(exc.errors(), exclude={"input"})
        return JSONResponse(
            status_code=422,
            content=fail("VALIDATION_ERROR", "Request validation failed.", {"errors": safe_errors}),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        logger.exception("unhandled_exception")
        return JSONResponse(
            status_code=500,
            content=fail("INTERNAL_ERROR", "An unexpected error occurred."),
        )

    # Routers, versioned under /api/v1
    app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(jobs_router, prefix=settings.API_V1_PREFIX)
    app.include_router(applications_router, prefix=settings.API_V1_PREFIX)
    app.include_router(ai_router, prefix=settings.API_V1_PREFIX)

    @app.get("/health", tags=["ops"])
    def health():
        """Liveness — is the process up? No dependency checks."""
        return {"status": "ok", "service": settings.APP_NAME}

    @app.get("/ready", tags=["ops"])
    def ready():
        """Readiness — can we actually serve traffic (DB reachable)?"""
        try:
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            return {"status": "ready", "database": "connected"}
        except Exception:
            logger.exception("readiness_check_failed")
            return JSONResponse(status_code=503, content={"status": "not_ready", "database": "unreachable"})

    return app


app = create_app()
