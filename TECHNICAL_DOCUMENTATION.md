# Technical Documentation: Fuzzy Entity Matching API

## 1. Motivation & Problem Statement

### Why Do We Need This App?

In many real-world applications, data about entities (such as companies, products, or people) is collected from multiple sources. These sources often use slightly different names, spellings, or formats for the same entity. For example:
- "Büro AG" vs. "Buro AG"
- "Acme Corporation" vs. "Acme Corp."
- "Büro Offices Berlin GmbH & Co. KG" vs. "Buro Offices Berlin GmbH & Co KG"

This inconsistency makes it difficult to:
- Deduplicate records
- Integrate data from different systems
- Ensure data quality in analytics, reporting, and compliance

**Manual matching is time-consuming, error-prone, and not scalable.**

The Fuzzy Entity Matching API automates this process, providing a robust, scalable, and explainable way to match and deduplicate entity names.

---

## 2. Use Cases

- **Data Integration:** Merging datasets from different sources (e.g., CRM, ERP, public registries)
- **Data Cleaning:** Deduplicating and standardizing entity names in large databases
- **Compliance:** Ensuring consistent naming for regulatory reporting
- **Search & Recommendation:** Suggesting likely matches for user-entered names
- **ETL Pipelines:** Automated entity resolution during data ingestion

---

## 3. Technical Logic & Architecture

### 3.1. Preprocessing

Before matching, all input and canonical entity names are preprocessed to:
- Remove diacritics (e.g., "Büro" → "Buro")
- Convert to lowercase
- Remove illegal/special characters (except &, -, .)
- Standardize common legal terms (e.g., "GmbH", "AG")

This normalization ensures that superficial differences do not affect the matching process.

### 3.2. Matching Algorithms

The core of the app is the `FuzzyMatcher` class, which combines multiple algorithms:

#### a) **TF-IDF Cosine Similarity**
- Converts all canonical entities and the query into TF-IDF vectors
- Measures cosine similarity between the query and each canonical entity
- Captures token-level similarity (e.g., "Acme Corp." vs. "Acme Corporation")

#### b) **Levenshtein Distance (Edit Distance)**
- Measures the minimum number of single-character edits required to change one string into another
- Captures typographical errors and small spelling differences

#### c) **Token Set Ratio**
- Compares sets of words in the strings, ignoring order and duplicates
- Useful for names with reordered or extra/missing words

#### d) **Weighted Scoring**
- The final confidence score is a weighted sum:
  - 40% TF-IDF cosine similarity
  - 40% Levenshtein ratio
  - 20% Token set ratio
- This balances semantic similarity, spelling, and word set overlap

### 3.3. Batch Processing

- Supports CSV and JSON file uploads for bulk matching
- Uses pandas for efficient data handling
- Returns a list of best matches for each input name

### 3.4. API Design

- **FastAPI** provides automatic OpenAPI/Swagger documentation
- **Pydantic** models ensure strict validation and clear API contracts
- **CORS** enabled for easy frontend integration
- **Health check** endpoint for monitoring

---

## 4. Extensibility & Customization

- **Canonical Entities Source:**
  - Currently hardcoded for demo; can be loaded from a database, file, or external API
- **Algorithm Weights:**
  - Can be tuned for specific domains or use cases
- **Additional Features:**
  - Add support for language detection, phonetic matching, or custom rules
  - Expose endpoints for managing canonical entities
- **Scalability:**
  - For large datasets, can integrate with vector search engines (e.g., FAISS, Annoy)

---

## 5. Design Decisions

- **Multiple Algorithms:** No single algorithm is perfect for all cases; combining them increases robustness
- **Explainability:** Returns detailed scores for transparency and debugging
- **Batch & Single Modes:** Supports both real-time and bulk workflows
- **OpenAPI Docs:** Ensures easy integration and discoverability
- **Python Ecosystem:** Leverages mature libraries for NLP and data processing

---

## 6. Security & Best Practices

- **Input Validation:** All inputs are validated using Pydantic
- **File Handling:** Only CSV and JSON files are accepted for batch processing
- **CORS:** Configured for safe frontend access (adjust in production)
- **Error Handling:** Returns clear error messages for unsupported file types or invalid input

---

## 7. Future Improvements

- Pluggable entity sources (DB, API, file)
- User authentication and authorization
- Real-time entity management (add/update/delete canonical entities)
- Advanced matching (phonetic, language-aware, etc.)
- Performance optimizations for very large datasets

---

## 8. References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [rapidfuzz Documentation](https://maxbachmann.github.io/RapidFuzz/)
- [pandas Documentation](https://pandas.pydata.org/)

---

**This technical documentation is intended for developers, architects, and data engineers who want to understand, extend, or integrate the Fuzzy Entity Matching API.** 