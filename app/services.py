"""
Service layer for business logic and file processing operations.
"""
import logging
import pandas as pd
import io
from typing import List, Dict, Any, Optional
from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse

from .config import (
    SUPPORTED_FILE_TYPES, 
    REQUIRED_CSV_COLUMN, 
    REQUIRED_JSON_FIELD, 
    ERROR_UNSUPPORTED_FILE_TYPE
)
from .matcher import FuzzyMatcher

# Configure logging
logger = logging.getLogger(__name__)


class FileProcessingService:
    """Service for handling file uploads and processing."""
    
    @staticmethod
    def validate_file_type(filename: str) -> bool:
        """
        Validate if the uploaded file type is supported.
        
        Args:
            filename: Name of the uploaded file
            
        Returns:
            True if file type is supported, False otherwise
        """
        if not filename:
            return False
        
        return any(filename.lower().endswith(ext) for ext in SUPPORTED_FILE_TYPES)
    
    @staticmethod
    def extract_names_from_file(file: UploadFile) -> List[str]:
        """
        Extract entity names from uploaded CSV or JSON file.
        
        Args:
            file: Uploaded file object
            
        Returns:
            List of entity names extracted from the file
            
        Raises:
            ValueError: If file format is invalid or required column/field is missing
            HTTPException: If file processing fails
        """
        try:
            content = file.file.read()
            filename = file.filename.lower() if file.filename else ""
            
            if not content:
                raise ValueError("File is empty")
            
            if filename.endswith('.csv'):
                return FileProcessingService._extract_from_csv(content)
            elif filename.endswith('.json'):
                return FileProcessingService._extract_from_json(content)
            else:
                raise ValueError(ERROR_UNSUPPORTED_FILE_TYPE)
                
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    
    @staticmethod
    def _extract_from_csv(content: bytes) -> List[str]:
        """Extract names from CSV content."""
        try:
            df = pd.read_csv(io.BytesIO(content))
            
            if REQUIRED_CSV_COLUMN not in df.columns:
                raise ValueError(f"CSV file must contain a '{REQUIRED_CSV_COLUMN}' column")
            
            names = df[REQUIRED_CSV_COLUMN].dropna().astype(str).tolist()
            
            if not names:
                raise ValueError("No valid names found in CSV file")
            
            return names
            
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty or invalid")
        except pd.errors.ParserError:
            raise ValueError("Invalid CSV format")
    
    @staticmethod
    def _extract_from_json(content: bytes) -> List[str]:
        """Extract names from JSON content."""
        try:
            df = pd.read_json(io.BytesIO(content))
            
            if REQUIRED_JSON_FIELD not in df.columns:
                raise ValueError(f"JSON file must contain a '{REQUIRED_JSON_FIELD}' field")
            
            names = df[REQUIRED_JSON_FIELD].dropna().astype(str).tolist()
            
            if not names:
                raise ValueError("No valid names found in JSON file")
            
            return names
            
        except ValueError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")


class MatchingService:
    """Service for entity matching operations."""
    
    def __init__(self, matcher: FuzzyMatcher):
        """
        Initialize the matching service.
        
        Args:
            matcher: Fuzzy matcher instance
        """
        self.matcher = matcher
        logger.info("MatchingService initialized successfully")
    
    def match_single_entity(self, query: str, top_n: int = 3) -> Dict[str, Any]:
        """
        Match a single entity against canonical entities.
        
        Args:
            query: Entity name to match
            top_n: Number of top matches to return
            
        Returns:
            Dictionary containing match results with query, top match, and alternatives
            
        Raises:
            ValueError: If query is empty or invalid
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        query = query.strip()
        logger.info(f"Matching single entity: {query}")
        
        try:
            results = self.matcher.match(query, top_n=top_n)
            
            # Convert scores to proper format for response
            def format_result(result: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    "entity": result["entity"],
                    "confidence": result["confidence"],
                    "scores": result["scores"]
                }
            
            response = {
                "query": query,
                "top_match": format_result(results[0]) if results else None,
                "alternatives": [format_result(r) for r in results[1:]]
            }
            
            logger.info(f"Successfully matched '{query}' with confidence {results[0]['confidence'] if results else 0}")
            return response
            
        except Exception as e:
            logger.error(f"Error matching entity '{query}': {str(e)}")
            raise
    
    def match_batch_entities(self, names: List[str]) -> List[Dict[str, Any]]:
        """
        Match a batch of entity names.
        
        Args:
            names: List of entity names to match
            
        Returns:
            List of match results for each input name
            
        Raises:
            ValueError: If names list is empty or contains invalid entries
        """
        if not names:
            raise ValueError("Names list cannot be empty")
        
        logger.info(f"Processing batch match for {len(names)} entities")
        
        results = []
        for i, name in enumerate(names):
            try:
                if not name or not name.strip():
                    logger.warning(f"Skipping empty name at index {i}")
                    continue
                
                name = name.strip()
                match = self.matcher.match(name, top_n=1)[0]
                
                results.append({
                    "input": name,
                    "match": match["entity"],
                    "confidence": match["confidence"]
                })
                
            except Exception as e:
                logger.error(f"Error matching entity '{name}' at index {i}: {str(e)}")
                # Continue processing other entities even if one fails
                results.append({
                    "input": name,
                    "match": None,
                    "confidence": 0.0,
                    "error": str(e)
                })
        
        logger.info(f"Completed batch match with {len(results)} results")
        return results 