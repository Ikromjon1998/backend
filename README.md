# Fuzzy Entity Matching API

A robust FastAPI-based service for fuzzy entity matching using multiple similarity algorithms. This API provides both single entity matching and batch processing capabilities with comprehensive error handling, logging, and configuration management.

## 🚀 Features

- **Multi-Algorithm Matching**: Combines TF-IDF, Levenshtein, and Token Set similarity
- **Batch Processing**: Upload CSV or JSON files for bulk entity matching
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Environment Configuration**: Flexible configuration via environment variables and `.env` file
- **Input Validation**: Robust validation with detailed error messages
- **Health Checks**: Built-in health monitoring endpoints
- **CORS Support**: Configurable CORS settings for frontend integration

## 📋 Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- scikit-learn
- rapidfuzz
- pandas
- pydantic
- pydantic-settings
- pytest (for testing)
- pytest-cov (for coverage)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fuzzy-entity-matching/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Install development dependencies**
   If you have a `requirements-dev.txt` or similar, install it for testing and development:
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env` (if `.env.example` does not exist, create it based on the configuration options in `app/config.py`):
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` with your configuration. All variables in `.env.example` are supported. Extra fields are ignored.

## 🏃‍♂️ Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## 🔧 Configuration

The application uses environment variables for configuration. Key settings include:

### API Configuration
- `API_TITLE`: API title (default: "Fuzzy Entity Matching API")
- `API_VERSION`: API version (default: "1.0.0")

### Matching Algorithm Weights
- `TFIDF_WEIGHT`: Weight for TF-IDF similarity (default: 0.4)
- `LEVENSHTEIN_WEIGHT`: Weight for Levenshtein similarity (default: 0.4)
- `TOKEN_SET_WEIGHT`: Weight for Token Set similarity (default: 0.2)

### File Processing
- `SUPPORTED_FILE_TYPES`: List of supported file extensions
- `REQUIRED_CSV_COLUMN`: Required column name for CSV files
- `REQUIRED_JSON_FIELD`: Required field name for JSON files

### Logging
- `LOG_LEVEL`: Logging level for the application (e.g., INFO, DEBUG, WARNING)
- Logging is configured in `app/logging_config.py` and logs to both stdout and `app.log` file.
- Extra fields in `.env` are ignored due to the config setting in `app/config.py`.

### Canonical Entities
- The canonical entities used for matching are currently hardcoded in `app/config.py` under the `canonical_entities` field. In production, you may want to load these from a database or external file.

## 📖 API Endpoints

### Single Entity Matching
```http
POST /match
Content-Type: application/json

{
  "query": "Buro AG"
}
```

**Request Body:**
- JSON object with a `query` field (string): the entity name to match.

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
  "alternatives": [...]
}
```

### Batch Entity Matching
```http
POST /match/batch
Content-Type: multipart/form-data

file: [CSV or JSON file with 'names' column/field]
```

**Request:**
- Upload a file (CSV or JSON) with a `names` column (CSV) or `names` field (JSON) containing the list of entity names to match.

**Response:**
```json
[
  {
    "input": "Buro AG",
    "match": "Büro AG",
    "confidence": 0.93,
    "scores": {
      "tfidf": 0.95,
      "levenshtein": 0.98,
      "token_set": 0.97
    }
  }
]
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=app tests/
```

**Note:** If you have a `requirements-dev.txt` or similar, install it before running tests:
```bash
pip install -r requirements-dev.txt
```

**Test files:**
- tests/test_matcher.py
- tests/test_preprocessor.py
- tests/test_api.py
- tests/test_services.py

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models for validation
│   ├── matcher.py           # Fuzzy matching algorithm
│   ├── preprocessor.py      # Text preprocessing utilities
│   ├── services.py          # Business logic layer
│   ├── routers.py           # API route definitions
│   └── logging_config.py    # Centralized logging configuration
├── tests/
│   ├── test_matcher.py
│   ├── test_preprocessor.py
│   ├── test_api.py
│   └── test_services.py
├── requirements.txt
├── sample.json              # Sample data for testing
├── sample.csv               # Sample data for testing
├── .env.example             # Example environment configuration
└── README.md
```

## 🔍 Code Quality Improvements

### 1. **Configuration Management**
- ✅ Environment variable support with Pydantic Settings
- ✅ Type-safe configuration with validation
- ✅ Default values with override capability

### 2. **Error Handling**
- ✅ Comprehensive exception handling
- ✅ Detailed error messages
- ✅ Graceful degradation for batch processing

### 3. **Logging**
- ✅ Structured logging throughout the application
- ✅ Different log levels (DEBUG, INFO, WARNING, ERROR)
- ✅ Request/response logging for debugging

### 4. **Code Organization**
- ✅ Clear separation of concerns
- ✅ Service layer for business logic
- ✅ Dependency injection

### 5. **Type Safety**
- ✅ Comprehensive type hints
- ✅ Pydantic models for validation
- ✅ Input/output validation

### 6. **Documentation**
- ✅ Detailed docstrings
- ✅ API documentation with examples
- ✅ Code comments for complex logic

### 7. **Testing**
- ✅ Unit tests for core functionality
- ✅ Integration tests for API endpoints
- ✅ Test coverage reporting

## 🚀 Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production
```bash
# Production settings
API_TITLE=Fuzzy Entity Matching API
API_VERSION=1.0.0
CORS_ORIGINS=["https://yourdomain.com"]
TFIDF_WEIGHT=0.4
LEVENSHTEIN_WEIGHT=0.4
TOKEN_SET_WEIGHT=0.2
LOG_LEVEL=INFO
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

---

**Note**: This API is designed for entity matching with a focus on German company names and legal entities. The preprocessing includes specific handling for German legal terms like "AG", "GmbH", etc. 

## 📝 Changelog

- See git history for recent changes. Add release notes here as needed.

## 📬 Contact

For questions, suggestions, or contributions, please open an issue or contact the maintainers via GitHub. 