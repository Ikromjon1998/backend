"""
Configuration settings for the Fuzzy Entity Matching API.
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    api_title: str = Field(default="Fuzzy Entity Matching API", description="API title")
    api_description: str = Field(
        default="This API provides fuzzy entity matching capabilities for single queries and batch uploads.",
        description="API description"
    )
    api_version: str = Field(default="1.0.0", description="API version")
    
    # CORS Configuration
    cors_origins: List[str] = Field(default=["*"], description="CORS allowed origins")
    cors_credentials: bool = Field(default=True, description="CORS credentials")
    cors_methods: List[str] = Field(default=["*"], description="CORS allowed methods")
    cors_headers: List[str] = Field(default=["*"], description="CORS allowed headers")
    
    # Matching Algorithm Configuration
    tfidf_weight: float = Field(default=0.4, ge=0.0, le=1.0, description="TF-IDF weight in matching algorithm")
    levenshtein_weight: float = Field(default=0.4, ge=0.0, le=1.0, description="Levenshtein weight in matching algorithm")
    token_set_weight: float = Field(default=0.2, ge=0.0, le=1.0, description="Token set weight in matching algorithm")
    
    # Default Matching Parameters
    default_top_n: int = Field(default=3, gt=0, le=10, description="Default number of top matches to return")
    
    # File Upload Configuration
    supported_file_types: List[str] = Field(default=[".csv", ".json"], description="Supported file types for upload")
    required_csv_column: str = Field(default="names", description="Required CSV column name")
    required_json_field: str = Field(default="names", description="Required JSON field name")
    
    # Error Messages
    error_unsupported_file_type: str = Field(
        default="Unsupported file type. Use CSV or JSON with a 'names' field.",
        description="Error message for unsupported file types"
    )
    
    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level for the application"
    )
    
    # Canonical Entities (in production, load from database or file)
    canonical_entities: List[str] = Field(
        default=[
            "Büro AG",
            "Büro GmbH", 
            "Büro Restaurants",
            "Büro Deutschland GmbH & Co. KG",
            "Büro Offices Berlin GmbH & Co. KG",
            "Büro Offices Solutions GmbH & Co. KG",
            "Büro Offices Solutions-Berlin GmbH & Co. KG"
        ],
        description="List of canonical entities for matching"
    )
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Create settings instance
settings = Settings()

# Export settings for backward compatibility
API_TITLE = settings.api_title
API_DESCRIPTION = settings.api_description
API_VERSION = settings.api_version
CORS_ORIGINS = settings.cors_origins
CORS_CREDENTIALS = settings.cors_credentials
CORS_METHODS = settings.cors_methods
CORS_HEADERS = settings.cors_headers
TFIDF_WEIGHT = settings.tfidf_weight
LEVENSHTEIN_WEIGHT = settings.levenshtein_weight
TOKEN_SET_WEIGHT = settings.token_set_weight
DEFAULT_TOP_N = settings.default_top_n
CANONICAL_ENTITIES = settings.canonical_entities
SUPPORTED_FILE_TYPES = settings.supported_file_types
REQUIRED_CSV_COLUMN = settings.required_csv_column
REQUIRED_JSON_FIELD = settings.required_json_field
ERROR_UNSUPPORTED_FILE_TYPE = settings.error_unsupported_file_type
LOG_LEVEL = settings.log_level 