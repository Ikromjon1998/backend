from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz
from .preprocessor import normalize_text, standardize_legal_terms

class FuzzyMatcher:
    def __init__(self, entities: list[str]):
        self.entities = entities
        # Preprocess entities for matching
        self.processed_entities = [
            standardize_legal_terms(normalize_text(e)) for e in entities
        ] # Normalize and standardize legal terms in entities. For example, "Büro AG" becomes "buro ag"
        self.vectorizer = TfidfVectorizer().fit(self.processed_entities)
        self.tfidf_matrix = self.vectorizer.transform(self.processed_entities)

    # Match entities against a query string using TF-IDF, Levenshtein, and token set ratios. top_n specifies how many results to return. Returns a list of dictionaries with entity, confidence score, and individual scores.
    def match(self, query: str, top_n: int = 3) -> list[dict]:
        # Preprocess query
        processed_query = standardize_legal_terms(normalize_text(query))
        # TF-IDF cosine similarity
        query_vec = self.vectorizer.transform([processed_query])
        tfidf_scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        # Levenshtein and token set ratios
        lev_scores = [fuzz.ratio(processed_query, e) / 100.0 for e in self.processed_entities] # Calculate Levenshtein ratio for each entity
        token_set_scores = [fuzz.token_set_ratio(processed_query, e) / 100.0 for e in self.processed_entities] # Calculate token set ratio for each entity
        # Combine scores
        results = []
        # Calculate combined score as a weighted average of the three scores
         # 40% TF-IDF, 40% Levenshtein, 20% token set ratio
        for idx, entity in enumerate(self.entities):
            score = 0.4 * tfidf_scores[idx] + 0.4 * lev_scores[idx] + 0.2 * token_set_scores[idx]

            # Append result with entity, confidence score, and individual scores
            results.append({
                "entity": entity,
                "confidence": round(score, 4),
                "scores": {
                    "tfidf": round(tfidf_scores[idx], 4),
                    "levenshtein": round(lev_scores[idx], 4),
                    "token_set": round(token_set_scores[idx], 4)
                }
            })
        # Sort by confidence descending
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results[:top_n]
