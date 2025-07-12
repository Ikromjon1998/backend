"""
API routers for organizing endpoints by functionality.
"""
import logging
from fastapi import APIRouter, UploadFile, File, status, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from .models import (
    MatchRequest, MatchResponse, BatchMatchResult,
    ErrorResponse, HealthResponse
)
from .services import MatchingService, FileProcessingService
from .config import DEFAULT_TOP_N

# Configure logging
logger = logging.getLogger(__name__)

# Create routers
matching_router = APIRouter(prefix="/match", tags=["Matching"])
health_router = APIRouter(prefix="/health", tags=["Health"])


def create_matching_router(matching_service: MatchingService) -> APIRouter:
    """
    Create matching router with dependency injection.

    Args:
        matching_service: Service instance for entity matching

    Returns:
        Configured APIRouter for matching endpoints
    """

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
                        "example": (getattr(MatchResponse, "model_config", {}) or {}).get(
                            "json_schema_extra", {}).get("example")
                    }
                }
            },
            400: {
                "model": ErrorResponse,
                "description": "Invalid request or query error."
            },
            422: {"description": "Validation Error"}
        }
    )
    def match_single_entity(request: MatchRequest) -> MatchResponse:
        """
        Fuzzy match a single entity name against canonical entities.

        - **query**: The entity name to match.
        - **Returns**: The best match and up to two alternatives, with confidence and detailed scores.
        """
        try:
            logger.info(f"Processing single entity match request: {request.query}")
            result = matching_service.match_single_entity(request.query, DEFAULT_TOP_N)
            logger.info(f"Successfully processed single entity match for: {request.query}")
            return MatchResponse(**result)

        except ValueError as e:
            logger.error(f"Validation error in single entity match: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error in single entity match: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

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
                        "example": [(getattr(BatchMatchResult, "model_config", {}) or {}).get(
                            "json_schema_extra", {}).get("example")]
                    }
                }
            },
            400: {
                "model": ErrorResponse,
                "description": "Unsupported file type or invalid file format.",
                "content": {
                    "application/json": {
                        "example": (getattr(ErrorResponse, "model_config", {}) or {}).get(
                            "json_schema_extra", {}).get("example")
                    }
                }
            },
            422: {"description": "Validation Error"}
        }
    )
    def match_batch_entities(
        file: UploadFile = File(..., description="CSV or JSON file with a 'names' column/field.")
    ):
        """
        Upload a CSV or JSON file with a 'names' column/field to batch match entity names.

        - **file**: CSV or JSON file with a 'names' column/field.
        - **Returns**: List of best matches for each input name, with confidence.
        - **Error**: Returns 400 if file type is not supported or format is invalid.
        """
        try:
            logger.info(f"Processing batch match request for file: {file.filename}")

            # Validate file type
            if not FileProcessingService.validate_file_type(file.filename or ""):
                error_msg = "Unsupported file type. Use CSV or JSON with a 'names' field."
                logger.warning(f"Unsupported file type: {file.filename}")
                return JSONResponse(
                    status_code=400,
                    content={"error": error_msg}
                )

            # Extract names from file
            names = FileProcessingService.extract_names_from_file(file)
            logger.info(f"Extracted {len(names)} names from file: {file.filename}")

            # Perform batch matching
            results = matching_service.match_batch_entities(names)
            logger.info(f"Successfully processed batch match with {len(results)} results")

            return [BatchMatchResult(**result) for result in results]

        except HTTPException:
            # Re-raise HTTP exceptions as they already have proper status codes
            raise
        except ValueError as e:
            logger.error(f"Validation error in batch match: {str(e)}")
            return JSONResponse(status_code=400, content={"error": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in batch match: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error during batch processing"}
            )

    return matching_router


def create_health_router() -> APIRouter:
    """
    Create health check router.

    Returns:
        Configured APIRouter for health check endpoints
    """

    @health_router.get(
        "",
        response_model=HealthResponse,
        summary="Health check",
        response_description="API health status.",
        responses={
            200: {
                "description": "API is running.",
                "content": {"application/json": {"example": {"status": "ok"}}}
            }
        }
    )
    def health_check() -> HealthResponse:
        """
        Simple health check endpoint to verify the API is running.
        """
        logger.debug("Health check requested")
        return HealthResponse(status="ok")

    return health_router
