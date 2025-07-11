import re
import unicodedata


def normalize_text(text: str) -> str:
    """
    Normalize text by removing diacritics, converting to lowercase, and stripping illegal characters.
    Keeps &, -, ., and alphanumeric characters.
    """
    # Remove diacritics
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    # Lowercase
    text = text.lower()
    # Strip illegal characters (keep &, -, ., alphanumeric, and spaces)
    text = re.sub(r"[^\w\s&\-.]", "", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def standardize_legal_terms(text: str) -> str:
    """
    Standardize common legal terms using regex replacements.
    """
    # AG
    text = re.sub(r"\b(ag|a\.g\.?|aktiengesellschaft)\b", "ag", text, flags=re.IGNORECASE)
    # GmbH
    text = re.sub(r"\b(gmbh|g\.m\.b\.h\.?)\b", "gmbh", text, flags=re.IGNORECASE)
    # and (improve & handling)
    text = re.sub(r"(\bund\b|\bu\.\b|(?<=\s)&(?=\s)|^&(?=\s)|(?<=\s)&$|^&$)", "and", text, flags=re.IGNORECASE)
    return text
