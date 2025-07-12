"""
Fuzzy entity matching implementation using multiple similarity algorithms.
"""
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz

from .preprocessor import normalize_text, standardize_legal_terms
from .config import TFIDF_WEIGHT, LEVENSHTEIN_WEIGHT, TOKEN_SET_WEIGHT


class FuzzyMatcher:
    """
    Fuzzy entity matcher using TF-IDF, Levenshtein, and token set similarity.
    
    This class provides fuzzy matching capabilities by combining multiple similarity
    algorithms to find the best matches for entity names against a set of canonical entities.
    """
    
    def __init__(self, entities: List[str]) -> None:
        """
        Initialize the fuzzy matcher with canonical entities.
        
        Args:
            entities: List of canonical entity names to match against
        """
        self.entities = entities
        self._initialize_matcher()
    
    def _initialize_matcher(self) -> None:
        """Initialize the TF-IDF vectorizer and preprocess entities."""
        # Preprocess entities for matching
        self.processed_entities = [
            standardize_legal_terms(normalize_text(entity)) 
            for entity in self.entities
        ]
        
        # Initialize and fit TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_entities)
    
    def match(self, query: str, top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Match a query against canonical entities using multiple similarity algorithms.
        
        Args:
            query: The entity name to match
            top_n: Number of top matches to return (default: 3)
            
        Returns:
            List of dictionaries containing match results with entity, confidence, and scores
            
        Raises:
            ValueError: If top_n is less than 1 or greater than the number of entities
        """
        if top_n < 1:
            raise ValueError("top_n must be at least 1")
        if top_n > len(self.entities):
            top_n = len(self.entities)
        
        # Preprocess query
        processed_query = standardize_legal_terms(normalize_text(query))
        
        # Calculate similarity scores
        tfidf_scores = self._calculate_tfidf_scores(processed_query)
        levenshtein_scores = self._calculate_levenshtein_scores(processed_query)
        token_set_scores = self._calculate_token_set_scores(processed_query)
        
        # Combine scores and create results
        results = self._combine_scores(
            tfidf_scores, levenshtein_scores, token_set_scores
        )
        
        # Sort by confidence and return top_n results
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results[:top_n]
    
    def _calculate_tfidf_scores(self, processed_query: str) -> List[float]:
        """Calculate TF-IDF cosine similarity scores."""
        query_vector = self.vectorizer.transform([processed_query])
        return cosine_similarity(query_vector, self.tfidf_matrix)[0].tolist()
    
    def _calculate_levenshtein_scores(self, processed_query: str) -> List[float]:
        """Calculate Levenshtein similarity scores."""
        return [
            fuzz.ratio(processed_query, entity) / 100.0 
            for entity in self.processed_entities
        ]
    
    def _calculate_token_set_scores(self, processed_query: str) -> List[float]:
        """Calculate token set similarity scores."""
        return [
            fuzz.token_set_ratio(processed_query, entity) / 100.0 
            for entity in self.processed_entities
        ]
    
    def _combine_scores(
        self, 
        tfidf_scores: List[float], 
        levenshtein_scores: List[float], 
        token_set_scores: List[float]
    ) -> List[Dict[str, Any]]:
        """
        Combine individual similarity scores using weighted average.
        
        Args:
            tfidf_scores: TF-IDF similarity scores
            levenshtein_scores: Levenshtein similarity scores  
            token_set_scores: Token set similarity scores
            
        Returns:
            List of result dictionaries with combined scores
        """
        results = []
        
        for idx, entity in enumerate(self.entities):
            # Calculate weighted average of all scores
            combined_score = (
                TFIDF_WEIGHT * tfidf_scores[idx] +
                LEVENSHTEIN_WEIGHT * levenshtein_scores[idx] +
                TOKEN_SET_WEIGHT * token_set_scores[idx]
            )
            
            results.append({
                "entity": entity,
                "confidence": round(combined_score, 4),
                "scores": {
                    "tfidf": round(tfidf_scores[idx], 4),
                    "levenshtein": round(levenshtein_scores[idx], 4),
                    "token_set": round(token_set_scores[idx], 4)
                }
            })
        
        return results
