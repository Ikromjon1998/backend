"""
Service layer for business logic and file processing operations.
"""
import pandas as pd
import io
from typing import List, Dict, Any
from fastapi import UploadFile
from fastapi.responses import JSONResponse

from .config import SUPPORTED_FILE_TYPES, REQUIRED_CSV_COLUMN, REQUIRED_JSON_FIELD, ERROR_UNSUPPORTED_FILE_TYPE
from .matcher import FuzzyMatcher

class FileProcessingService:
    """Service for handling file uploads and processing."""
    
    @staticmethod
    def validate_file_type(filename: str) -> bool:
        """Validate if the uploaded file type is supported."""
        return any(filename.lower().endswith(ext) for ext in SUPPORTED_FILE_TYPES)
    
    @staticmethod
    def extract_names_from_file(file: UploadFile) -> List[str]:
        """Extract entity names from uploaded CSV or JSON file."""
        content = file.file.read()
        filename = file.filename.lower()
        
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
            if REQUIRED_CSV_COLUMN not in df.columns:
                raise ValueError(f"CSV file must contain a '{REQUIRED_CSV_COLUMN}' column")
            return df[REQUIRED_CSV_COLUMN].tolist()
        
        elif filename.endswith('.json'):
            df = pd.read_json(io.BytesIO(content))
            if REQUIRED_JSON_FIELD not in df.columns:
                raise ValueError(f"JSON file must contain a '{REQUIRED_JSON_FIELD}' field")
            return df[REQUIRED_JSON_FIELD].tolist()
        
        else:
            raise ValueError(ERROR_UNSUPPORTED_FILE_TYPE)

class MatchingService:
    """Service for entity matching operations."""
    
    def __init__(self, matcher: FuzzyMatcher):
        self.matcher = matcher
    
    def match_single_entity(self, query: str, top_n: int = 3) -> Dict[str, Any]:
        """Match a single entity against canonical entities."""
        results = self.matcher.match(query, top_n=top_n)
        
        # Convert scores to proper format for response
        def to_result(r):
            return {
                "entity": r["entity"],
                "confidence": r["confidence"],
                "scores": r["scores"]
            }
        
        return {
            "query": query,
            "top_match": to_result(results[0]),
            "alternatives": [to_result(r) for r in results[1:]]
        }
    
    def match_batch_entities(self, names: List[str]) -> List[Dict[str, Any]]:
        """Match a batch of entity names."""
        results = []
        for name in names:
            match = self.matcher.match(name, top_n=1)[0]
            results.append({
                "input": name,
                "match": match["entity"],
                "confidence": match["confidence"]
            })
        return results 