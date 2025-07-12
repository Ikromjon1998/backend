"""
Pydantic models for request/response validation and API documentation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class ScoreDetail(BaseModel):
    """Detailed similarity scores for each matching algorithm."""
    
    tfidf: float = Field(
        ..., 
        json_schema_extra={"example": 0.95, "description": "TF-IDF similarity score."}
    )
    levenshtein: float = Field(
        ..., 
        json_schema_extra={"example": 0.98, "description": "Levenshtein similarity score."}
    )
    token_set: float = Field(
        ..., 
        json_schema_extra={"example": 0.97, "description": "Token set similarity score."}
    )

    class Config:
        json_schema_extra = {
            "example": {"tfidf": 0.95, "levenshtein": 0.98, "token_set": 0.97}
        }


class MatchRequest(BaseModel):
    """Request model for single entity matching."""
    
    query: str = Field(
        ..., 
        json_schema_extra={"example": "Buro AG", "description": "The entity name to match."}
    )
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        """Validate that query is not empty after trimming."""
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {"query": "Buro AG"}
        }


class MatchResult(BaseModel):
    """Result model for a single entity match."""
    
    entity: str = Field(
        ..., 
        json_schema_extra={"example": "Büro AG", "description": "The matched canonical entity."}
    )
    confidence: float = Field(
        ..., 
        json_schema_extra={"example": 0.98, "description": "Overall confidence score for the match."}
    )
    scores: ScoreDetail = Field(
        ..., 
        json_schema_extra={"description": "Detailed similarity scores."}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "entity": "Büro AG",
                "confidence": 0.98,
                "scores": {"tfidf": 0.95, "levenshtein": 0.98, "token_set": 0.97}
            }
        }


class MatchResponse(BaseModel):
    """Response model for single entity matching."""
    
    query: str = Field(
        ..., 
        json_schema_extra={"example": "Buro AG", "description": "The original query string."}
    )
    top_match: Optional[MatchResult] = Field(
        ..., 
        json_schema_extra={"description": "The best match for the query."}
    )
    alternatives: List[MatchResult] = Field(
        default=[], 
        json_schema_extra={"description": "Alternative matches."}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Buro AG",
                "top_match": {
                    "entity": "Büro AG",
                    "confidence": 0.98,
                    "scores": {"tfidf": 0.95, "levenshtein": 0.98, "token_set": 0.97}
                },
                "alternatives": [
                    {
                        "entity": "Büro Offices Berlin GmbH & Co. KG",
                        "confidence": 0.85,
                        "scores": {"tfidf": 0.80, "levenshtein": 0.84, "token_set": 0.83}
                    },
                    {
                        "entity": "Büro GmbH",
                        "confidence": 0.60,
                        "scores": {"tfidf": 0.55, "levenshtein": 0.62, "token_set": 0.63}
                    }
                ]
            }
        }


class BatchMatchResult(BaseModel):
    """Result model for batch entity matching."""
    
    input: str = Field(
        ..., 
        json_schema_extra={"example": "Buro AG", "description": "The input name from the file."}
    )
    match: Optional[str] = Field(
        None, 
        json_schema_extra={"example": "Büro AG", "description": "The best matched canonical entity."}
    )
    confidence: float = Field(
        ..., 
        json_schema_extra={"example": 0.93, "description": "Confidence score for the match."}
    )
    error: Optional[str] = Field(
        None, 
        json_schema_extra={"description": "Error message if matching failed."}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "input": "Buro AG",
                "match": "Büro AG",
                "confidence": 0.93
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(
        ..., 
        json_schema_extra={
            "example": "Unsupported file type. Use CSV or JSON with a 'names' field.",
            "description": "Error message describing what went wrong."
        }
    )

    class Config:
        json_schema_extra = {
            "example": {"error": "Unsupported file type. Use CSV or JSON with a 'names' field."}
        }


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(
        ..., 
        json_schema_extra={"example": "ok", "description": "API health status."}
    )
    
    class Config:
        json_schema_extra = {
            "example": {"status": "ok"}
        } 