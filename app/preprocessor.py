"""
Text preprocessing utilities for entity matching.
"""
import re
from typing import List


def normalize_text(text: str) -> str:
    """
    Normalize text for matching by converting to lowercase and removing extra whitespace.

    Args:
        text: Input text to normalize

    Returns:
        Normalized text string
    """
    if not text:
        return ""

    # Convert to lowercase and strip whitespace
    normalized = text.lower().strip()

    # Replace multiple whitespace with single space
    normalized = re.sub(r'\s+', ' ', normalized)

    return normalized


def standardize_legal_terms(text: str) -> str:
    """
    Standardize common legal terms and abbreviations.

    Args:
        text: Input text containing legal terms

    Returns:
        Text with standardized legal terms
    """
    if not text:
        return ""

    # Common legal term mappings
    legal_terms = {
        'g.m.b.h': 'gmbh',
        'gmbh': 'gmbh',
        'aktiengesellschaft': 'ag',
        'ag': 'ag',
        'und': 'and',
        '&': 'and',
        'co.': 'co',
        'kg': 'kg',
        'limited': 'ltd',
        'ltd.': 'ltd',
        'incorporated': 'inc',
        'inc.': 'inc',
        'corporation': 'corp',
        'corp.': 'corp'
    }

    # Split text into words and standardize each
    words = text.split()
    standardized_words = []

    for word in words:
        # Remove punctuation and convert to lowercase
        clean_word = re.sub(r'[^\w\s]', '', word.lower())
        # Apply legal term standardization
        standardized_word = legal_terms.get(clean_word, word)
        standardized_words.append(standardized_word)

    return ' '.join(standardized_words)


def preprocess_entity_name(entity_name: str) -> str:
    """
    Complete preprocessing pipeline for entity names.

    Args:
        entity_name: Raw entity name

    Returns:
        Preprocessed entity name ready for matching
    """
    if not entity_name:
        return ""

    # Step 1: Normalize text
    normalized = normalize_text(entity_name)

    # Step 2: Standardize legal terms
    standardized = standardize_legal_terms(normalized)

    return standardized


def extract_company_suffixes(text: str) -> List[str]:
    """
    Extract common company suffixes from text.

    Args:
        text: Input text

    Returns:
        List of found company suffixes
    """
    suffixes = ['ag', 'gmbh', 'kg', 'ltd', 'inc', 'corp', 'llc']
    found_suffixes = []

    normalized_text = text.lower()
    for suffix in suffixes:
        if suffix in normalized_text:
            found_suffixes.append(suffix)

    return found_suffixes


def remove_common_words(text: str) -> str:
    """
    Remove common words that don't add meaning to entity names.

    Args:
        text: Input text

    Returns:
        Text with common words removed
    """
    common_words = {
        'the', 'and', 'or', 'of', 'for', 'in', 'on', 'at', 'to', 'from',
        'with', 'by', 'about', 'like', 'through', 'over', 'before', 'after',
        'between', 'among', 'during', 'within', 'without', 'against', 'toward',
        'towards', 'up', 'down', 'out', 'off', 'on', 'away', 'back', 'forward'
    }

    words = text.split()
    filtered_words = [word for word in words if word.lower() not in common_words]

    return ' '.join(filtered_words)

