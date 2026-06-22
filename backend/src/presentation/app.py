"""
Automatic Workflow - FastAPI Application
Main application factory and entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.presentation.routes import (
    workflow_routes,
    auth_routes,
    integration_routes,
    chat_routes
)
from src.presentation.middleware.error_handler import ErrorHandlerMiddleware
from src.infrastructure.database.postgres_repository import init_database
from src.infrastructure.cache.redis_cache import init_redis
from src.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting Automatic Workflow API...")
    
    # Initialize database
    try:
        await init_database()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"Database initialization skipped: {e}")
    
    # Initialize Redis
    try:
        await init_redis()
        logger.info("Redis cache initialized")
    except Exception as e:
        logger.warning(f"Redis initialization skipped: {e}")
    
    yield
    
    logger.info("Shutting down Automatic Workflow API...")


# Create FastAPI application
app = FastAPI(
    title="Automatic Workflow API",
    description="API for building and managing automated workflows",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handler middleware
app.add_middleware(ErrorHandlerMiddleware)

# Include routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(workflow_routes.router, prefix="/api/v1/workflows", tags=["Workflows"])
app.include_router(integration_routes.router, prefix="/api/v1/integrations", tags=["Integrations"])
app.include_router(chat_routes.router, prefix="/api/v1/chat", tags=["Chat"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Automatic Workflow API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# For Vercel serverless function
handler = app
