from fastapi import FastAPI, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import pandas as pd
from app.matcher import FuzzyMatcher
import io

app = FastAPI(
    title="Fuzzy Entity Matching API",
    description="""
    This API provides fuzzy entity matching capabilities for single queries and batch uploads.\n\n
    - **/match**: Fuzzy match a single entity name against canonical entities.\n
    - **/batch-match**: Upload a CSV or JSON file with a list of names to batch match.\n
    - **/health**: Health check endpoint.
    """,
    version="1.0.0"
)

# Allow CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoreDetail(BaseModel):
    tfidf: float = Field(..., example=0.95, description="TF-IDF similarity score.")
    levenshtein: float = Field(..., example=0.98, description="Levenshtein similarity score.")
    token_set: float = Field(..., example=0.97, description="Token set similarity score.")

    class Config:
        json_schema_extra = {
            "example": {"tfidf": 0.95, "levenshtein": 0.98, "token_set": 0.97}
        }

class MatchRequest(BaseModel):
    query: str = Field(..., example="Buro AG", description="The entity name to match.")

    class Config:
        json_schema_extra = {
            "example": {"query": "Buro AG"}
        }

class MatchResult(BaseModel):
    entity: str = Field(..., example="Büro AG", description="The matched canonical entity.")
    confidence: float = Field(..., example=0.98, description="Overall confidence score for the match.")
    scores: ScoreDetail = Field(..., description="Detailed similarity scores.")

    class Config:
        json_schema_extra = {
            "example": {
                "entity": "Büro AG",
                "confidence": 0.98,
                "scores": {"tfidf": 0.95, "levenshtein": 0.98, "token_set": 0.97}
            }
        }

class MatchResponse(BaseModel):
    query: str = Field(..., example="Buro AG", description="The original query string.")
    top_match: MatchResult = Field(..., description="The best match for the query.")
    alternatives: List[MatchResult] = Field(..., description="Alternative matches.")

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
                        "entity": "Acme Corporation",
                        "confidence": 0.60,
                        "scores": {"tfidf": 0.55, "levenshtein": 0.62, "token_set": 0.63}
                    }
                ]
            }
        }

class BatchMatchResult(BaseModel):
    input: str = Field(..., example="Acme Corp.", description="The input name from the file.")
    match: str = Field(..., example="Acme Corporation", description="The best matched canonical entity.")
    confidence: float = Field(..., example=0.93, description="Confidence score for the match.")

    class Config:
        json_schema_extra = {
            "example": {
                "input": "Acme Corp.",
                "match": "Acme Corporation",
                "confidence": 0.93
            }
        }

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Unsupported file type. Use CSV or JSON with a 'names' field.")

    class Config:
        json_schema_extra = {
            "example": {"error": "Unsupported file type. Use CSV or JSON with a 'names' field."}
        }

@app.post(
    "/match",
    response_model=MatchResponse,
    status_code=status.HTTP_200_OK,
    summary="Fuzzy match a single entity name",
    response_description="The best match and alternatives for the query.",
    tags=["Matching"],
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
def match(request: MatchRequest):
    """
    Fuzzy match a single entity name against canonical entities.

    - **query**: The entity name to match.
    - **Returns**: The best match and up to two alternatives, with confidence and detailed scores.
    """
    results = matcher.match(request.query, top_n=3)
    # Convert scores to ScoreDetail for OpenAPI
    def to_result(r):
        return {
            "entity": r["entity"],
            "confidence": r["confidence"],
            "scores": r["scores"]
        }
    return {
        "query": request.query,
        "top_match": to_result(results[0]),
        "alternatives": [to_result(r) for r in results[1:]]
    }

@app.post(
    "/batch-match",
    response_model=List[BatchMatchResult],
    status_code=status.HTTP_200_OK,
    summary="Batch fuzzy match from file upload",
    response_description="A list of best matches for each input name.",
    tags=["Matching"],
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
            "description": "Unsupported file type. Use CSV or JSON with a 'names' field.",
            "content": {
                "application/json": {
                    "example": ErrorResponse.Config.json_schema_extra["example"]
                }
            }
        },
        422: {"description": "Validation Error"}
    }
)
def batch_match(file: UploadFile = File(..., description="CSV or JSON file with a 'names' column/field.")):
    """
    Upload a CSV or JSON file with a 'names' column/field to batch match entity names.

    - **file**: CSV or JSON file with a 'names' column/field.
    - **Returns**: List of best matches for each input name, with confidence.
    - **Error**: Returns 400 if file type is not supported.
    """
    content = file.file.read()
    filename = file.filename.lower()
    if filename.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(content))
        names = df['names'].tolist()
    elif filename.endswith('.json'):
        df = pd.read_json(io.BytesIO(content))
        names = df['names'].tolist()
    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type. Use CSV or JSON with a 'names' field."})
    results = []
    for name in names:
        match = matcher.match(name, top_n=1)[0]
        results.append({
            "input": name,
            "match": match["entity"],
            "confidence": match["confidence"]
        })
    return results

@app.get(
    "/health",
    summary="Health check",
    response_description="API health status.",
    tags=["Health"],
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

# For demo: sample canonical entities (replace with file/db load in prod)
CANONICAL_ENTITIES = [
    "Büro AG",
    "Büro Offices Berlin GmbH & Co. KG",
    "Acme Corporation",
    "Test Entity GmbH"
]
matcher = FuzzyMatcher(CANONICAL_ENTITIES)
