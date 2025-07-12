"""
API routers for organizing endpoints by functionality.
"""
from fastapi import APIRouter, UploadFile, File, status, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from .models import (
    MatchRequest, MatchResponse, BatchMatchResult, 
    ErrorResponse, HealthResponse
)
from .services import MatchingService, FileProcessingService
from .config import DEFAULT_TOP_N

# Create routers
matching_router = APIRouter(prefix="/match", tags=["Matching"])
health_router = APIRouter(prefix="/health", tags=["Health"])

def create_matching_router(matching_service: MatchingService) -> APIRouter:
    """Create matching router with dependency injection."""
    
    @matching_router.post(
        "",
        response_model=MatchResponse,
        status_code=status.HTTP_200_OK,
        summary="Fuzzy match a single entity name",
        response_description="The best match and alternatives for the query.",
        responses={
            200: {
                "description": "Successful match result.",
                "content": {
                    "application/json": {
                        "example": MatchResponse.Config.json_schema_extra["example"]
                    }
                }
            },
            422: {"description": "Validation Error"}
        }
    )
    def match_single_entity(request: MatchRequest):
        """
        Fuzzy match a single entity name against canonical entities.

        - **query**: The entity name to match.
        - **Returns**: The best match and up to two alternatives, with confidence and detailed scores.
        """
        return matching_service.match_single_entity(request.query, DEFAULT_TOP_N)

    @matching_router.post(
        "/batch",
        response_model=List[BatchMatchResult],
        status_code=status.HTTP_200_OK,
        summary="Batch fuzzy match from file upload",
        response_description="A list of best matches for each input name.",
        responses={
            200: {
                "description": "Batch match results.",
                "content": {
                    "application/json": {
                        "example": [BatchMatchResult.Config.json_schema_extra["example"]]
                    }
                }
            },
            400: {
                "model": ErrorResponse,
                "description": "Unsupported file type or invalid file format.",
                "content": {
                    "application/json": {
                        "example": ErrorResponse.Config.json_schema_extra["example"]
                    }
                }
            },
            422: {"description": "Validation Error"}
        }
    )
    def match_batch_entities(file: UploadFile = File(..., description="CSV or JSON file with a 'names' column/field.")):
        """
        Upload a CSV or JSON file with a 'names' column/field to batch match entity names.

        - **file**: CSV or JSON file with a 'names' column/field.
        - **Returns**: List of best matches for each input name, with confidence.
        - **Error**: Returns 400 if file type is not supported or format is invalid.
        """
        try:
            # Validate file type
            if not FileProcessingService.validate_file_type(file.filename):
                return JSONResponse(
                    status_code=400, 
                    content={"error": "Unsupported file type. Use CSV or JSON with a 'names' field."}
                )
            
            # Extract names from file
            names = FileProcessingService.extract_names_from_file(file)
            
            # Perform batch matching
            results = matching_service.match_batch_entities(names)
            return results
            
        except ValueError as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        except Exception as e:
            return JSONResponse(
                status_code=400, 
                content={"error": f"Error processing file: {str(e)}"}
            )

    return matching_router

def create_health_router() -> APIRouter:
    """Create health check router."""
    
    @health_router.get(
        "",
        summary="Health check",
        response_description="API health status.",
        responses={
            200: {
                "description": "API is running.",
                "content": {"application/json": {"example": {"status": "ok"}}}
            }
        }
    )
    def health_check():
        """
        Simple health check endpoint to verify the API is running.
        """
        return {"status": "ok"}

    return health_router 