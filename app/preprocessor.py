"""
Text preprocessing utilities for entity matching.
"""
import re
import unicodedata
from typing import Dict, Pattern


def normalize_text(text: str) -> str:
    """
    Normalize text by removing diacritics, converting to lowercase, and stripping illegal characters.
    
    This function performs the following transformations:
    - Removes diacritics (accents, umlauts, etc.)
    - Converts to lowercase
    - Strips illegal characters (keeps &, -, ., alphanumeric, and spaces)
    - Collapses multiple spaces into single spaces
    - Trims leading and trailing whitespace
    
    Args:
        text: Input text to normalize
        
    Returns:
        Normalized text string
        
    Examples:
        >>> normalize_text("Büro A.G.")
        "buro a.g."
        >>> normalize_text("  Büro   GmbH  ")
        "buro gmbh"
    """
    if not text:
        return ""
    
    # Remove diacritics
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    
    # Convert to lowercase
    text = text.lower()
    
    # Strip illegal characters (keep &, -, ., alphanumeric, and spaces)
    text = re.sub(r"[^\w\s&\-.]", "", text)
    
    # Collapse multiple spaces and trim
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def standardize_legal_terms(text: str) -> str:
    """
    Standardize common legal terms using regex replacements.
    
    This function standardizes common legal entity suffixes and terms:
    - AG, A.G., Aktiengesellschaft → ag
    - GmbH, G.M.B.H. → gmbh
    - "und", "u.", "&" → "and"
    
    Args:
        text: Input text to standardize
        
    Returns:
        Text with standardized legal terms
        
    Examples:
        >>> standardize_legal_terms("Büro A.G.")
        "buro ag"
        >>> standardize_legal_terms("Büro GmbH & Co KG")
        "buro gmbh and co kg"
    """
    if not text:
        return ""
    
    # Standardize AG variations
    text = re.sub(r"\b(ag|a\.g\.?|aktiengesellschaft)\b", "ag", text, flags=re.IGNORECASE)
    
    # Standardize GmbH variations
    text = re.sub(r"\b(gmbh|g\.m\.b\.h\.?)\b", "gmbh", text, flags=re.IGNORECASE)
    
    # Standardize "and" variations
    text = re.sub(
        r"(\bund\b|\bu\.\b|(?<=\s)&(?=\s)|^&(?=\s)|(?<=\s)&$|^&$)", 
        "and", 
        text, 
        flags=re.IGNORECASE
    )
    
    return text


def preprocess_entity_name(text: str) -> str:
    """
    Complete preprocessing pipeline for entity names.
    
    This function combines normalization and legal term standardization
    to prepare entity names for fuzzy matching.
    
    Args:
        text: Raw entity name to preprocess
        
    Returns:
        Preprocessed entity name ready for matching
        
    Examples:
        >>> preprocess_entity_name("Büro A.G.")
        "buro ag"
        >>> preprocess_entity_name("Büro GmbH & Co. KG")
        "buro gmbh and co kg"
    """
    if not text:
        return ""
    
    # Apply normalization first
    normalized = normalize_text(text)
    
    # Then apply legal term standardization
    standardized = standardize_legal_terms(normalized)
    
    return standardized
