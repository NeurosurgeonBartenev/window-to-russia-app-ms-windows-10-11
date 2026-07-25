#!/usr/bin/env python3
"""
Window to RUSSIA Backend API
Main entry point for the FastAPI application
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config.settings import settings
from src.database.database import Base, engine

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")
    await engine.dispose()
    logger.info("Database connection closed")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="API for Window to RUSSIA wallpaper application",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# Health check endpoint
@app.get("/health")
async def health_check() -> JSONResponse:
    """
    Health check endpoint
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT
        }
    )


@app.get("/")
async def root() -> JSONResponse:
    """
    Root endpoint with API information
    """
    return JSONResponse(
        status_code=200,
        content={
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": "Window to RUSSIA - Wallpaper Application API",
            "docs": "/api/docs",
            "redoc": "/api/redoc",
            "health": "/health"
        }
    )


# API v1 routes (will be added)
# @app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
# @app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
# @app.include_router(themes_router, prefix="/api/v1/themes", tags=["themes"])
# @app.include_router(wallpapers_router, prefix="/api/v1/wallpapers", tags=["wallpapers"])
# @app.include_router(favorites_router, prefix="/api/v1/favorites", tags=["favorites"])


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Handle general exceptions
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc) if settings.DEBUG else None}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
