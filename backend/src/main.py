from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

# Import routers
from api.auth import router as auth_router
from api.wallpapers import router as wallpapers_router
from api.users import router as users_router
from api.favorites import router as favorites_router
from api.places import router as places_router
from api.subscriptions import router as subscriptions_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application startup")
    yield
    # Shutdown
    logger.info("Application shutdown")

# Create FastAPI app
app = FastAPI(
    title="Window to RUSSIA API",
    description="API for Window to RUSSIA wallpaper application",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(wallpapers_router, prefix="/api/v1/wallpapers", tags=["Wallpapers"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(favorites_router, prefix="/api/v1/favorites", tags=["Favorites"])
app.include_router(places_router, prefix="/api/v1/places", tags=["Places"])
app.include_router(subscriptions_router, prefix="/api/v1/subscriptions", tags=["Subscriptions"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "app": "Window to RUSSIA API",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
