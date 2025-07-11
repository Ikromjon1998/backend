# Fuzzy Entity Matching API

A FastAPI-based REST API for fuzzy matching of entity names against canonical entities. This service provides both single-query matching and batch processing capabilities with detailed confidence scores.

## Features

- **Single Entity Matching**: Match individual entity names against a canonical list
- **Batch Processing**: Upload CSV or JSON files for bulk entity matching
- **Multiple Similarity Algorithms**: Combines TF-IDF, Levenshtein distance, and token set similarity
- **Detailed Scoring**: Provides confidence scores and detailed similarity breakdowns
- **Interactive API Documentation**: Built-in Swagger UI and OpenAPI specification
- **CORS Support**: Ready for frontend integration

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **scikit-learn**: TF-IDF vectorization and cosine similarity
- **rapidfuzz**: Fast fuzzy string matching algorithms
- **pandas**: Data processing for batch operations
- **uvicorn**: ASGI server for production deployment

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fuzzy-entity-matching/backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
   ```

5. **Access the API**
   - API Documentation: http://127.0.0.1:8080/docs
   - Health Check: http://127.0.0.1:8080/health

## API Endpoints

### 1. Single Entity Matching

**POST** `/match`

Match a single entity name against canonical entities.

**Request:**
```json
{
  "query": "Buro AG"
}
```

**Response:**
```json
{
  "query": "Buro AG",
  "top_match": {
    "entity": "Büro AG",
    "confidence": 0.98,
    "scores": {
      "tfidf": 0.95,
      "levenshtein": 0.98,
      "token_set": 0.97
    }
  },
  "alternatives": [
    {
      "entity": "Büro Offices Berlin GmbH & Co. KG",
      "confidence": 0.85,
      "scores": {
        "tfidf": 0.80,
        "levenshtein": 0.84,
        "token_set": 0.83
      }
    }
  ]
}
```

### 2. Batch Entity Matching

**POST** `/batch-match`

Upload a CSV or JSON file with entity names for batch processing.

**File Format:**
- **CSV**: Must have a `names` column
- **JSON**: Must have a `names` field (array of strings)

**Example CSV:**
```csv
names
Acme Corp.
Buro AG
Test Entity
```

**Example JSON:**
```json
{
  "names": ["Acme Corp.", "Buro AG", "Test Entity"]
}
```

**Response:**
```json
[
  {
    "input": "Acme Corp.",
    "match": "Acme Corporation",
    "confidence": 0.93
  },
  {
    "input": "Buro AG",
    "match": "Büro AG",
    "confidence": 0.98
  }
]
```

### 3. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "ok"
}
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and endpoints
│   ├── matcher.py           # Fuzzy matching logic
│   └── preprocessor.py      # Text preprocessing utilities
├── tests/
│   ├── test_matcher.py      # Unit tests for matcher
│   └── test_preprocessor.py # Unit tests for preprocessor
├── requirements.txt          # Python dependencies
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## Configuration

### Canonical Entities

The current implementation uses a hardcoded list of canonical entities. In production, you should:

1. Load entities from a database
2. Use a configuration file
3. Implement entity management endpoints

**Current entities:**
- Büro AG
- Büro Offices Berlin GmbH & Co. KG
- Acme Corporation
- Test Entity GmbH

### Matching Algorithm

The fuzzy matching combines three similarity metrics:

1. **TF-IDF Cosine Similarity** (40% weight)
2. **Levenshtein Distance** (40% weight)
3. **Token Set Ratio** (20% weight)

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

The project follows Python best practices with:
- Type hints
- Docstrings
- Unit tests
- Pydantic models for validation

### Adding New Features

1. **New Endpoints**: Add to `app/main.py`
2. **Matching Logic**: Modify `app/matcher.py`
3. **Text Processing**: Update `app/preprocessor.py`
4. **Tests**: Add corresponding test files

## Deployment

### Production Setup

1. **Environment Variables**
   ```bash
   export CANONICAL_ENTITIES_FILE=/path/to/entities.json
   export LOG_LEVEL=INFO
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Docker Deployment**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

## API Documentation

- **Interactive Docs**: http://127.0.0.1:8080/docs
- **OpenAPI Spec**: http://127.0.0.1:8080/openapi.json
- **ReDoc**: http://127.0.0.1:8080/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Add your license here]

## Support

For questions or issues, please [create an issue](link-to-issues) or contact the development team. 