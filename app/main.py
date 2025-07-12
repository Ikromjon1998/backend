"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import (
    API_TITLE, API_DESCRIPTION, API_VERSION,
    CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS,
    CANONICAL_ENTITIES
)
from .matcher import FuzzyMatcher
from .services import MatchingService
from .routers import create_matching_router, create_health_router

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Create FastAPI app
    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_CREDENTIALS,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )

    # Initialize services
    matcher = FuzzyMatcher(CANONICAL_ENTITIES)
    matching_service = MatchingService(matcher)

    # Create and include routers
    matching_router = create_matching_router(matching_service)
    health_router = create_health_router()
    
    app.include_router(matching_router)
    app.include_router(health_router)

    return app

# Create the application instance
app = create_app()
