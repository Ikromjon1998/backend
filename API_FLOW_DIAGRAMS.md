# Fuzzy Entity Matching API – Conceptual & Endpoint Flow Diagrams

## 1. System Overview

```mermaid
flowchart TD
    subgraph Client
        A1[Web Frontend / API Consumer]
    end
    subgraph Backend
        B1[FastAPI Router]
        B2[Request Validation - Pydantic]
        B3[MatchingService / FileProcessingService]
        B4[FuzzyMatcher]
        B5[Logging & Error Handling]
        B6[Response Models]
    end
    subgraph Infra
        C1[Config - .env, Settings]
        C2[Logging - app.log, stdout]
    end

    A1 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B3 --> B5
    B4 --> B3
    B3 --> B6
    B6 --> B1
    B1 --> A1
    B1 --> B5
    B5 --> C2
    B3 --> C1
```

---

## 2. Health Check (`GET /health`)

```mermaid
flowchart TD
    A[Client] -->|GET /health| B[FastAPI Router]
    B --> C[Health Check Handler]
    C --> D[Return - 'status': 'ok']
    C --> E[Log health check request]
```

---

## 3. Single Entity Match (`POST /match`)

```mermaid
flowchart TD
    A[Client] -->|POST /match with query| B[FastAPI Router]
    B --> C[Validate Request - Pydantic]
    C -->|Invalid| E1[Return 400/422 Error]
    C -->|Valid| D[MatchingService.match_single_entity]
    D --> F[FuzzyMatcher.match]
    F --> G[Compute Scores - TF-IDF, Levenshtein, Token Set]
    G --> H[Aggregate Results]
    H --> I[Return MatchResponse - top_match, alternatives, scores]
    D --> J[Log request & result]
    E1 --> J
```

---

## 4. Batch Entity Match (`POST /match/batch`)

```mermaid
flowchart TD
    A[Client] -->|POST /match/batch - CSV/JSON file | B[FastAPI Router]
    B --> C[Validate File Type]
    C -->|Invalid| E1[Return 400 Error]
    C --> D[Extract Names from File]
    D -->|Invalid| E2[Return 400 Error]
    D --> F[MatchingService.match_batch_entities]
    F --> G[For Each Name: FuzzyMatcher.match]
    G --> H[Compute Scores - TF-IDF, Levenshtein, Token Set]
    H --> I[Aggregate Batch Results]
    I --> J[Return List of BatchMatchResult - with scores]
    F --> K[Log batch request & results]
    E1 --> K
    E2 --> K
```

---

## 5. Error Handling & Logging

```mermaid
flowchart TD
    subgraph API
        A[Request Handler]
        B[Validation/Error]
        C[Service Layer]
        D[Exception Handler]
    end
    subgraph Infra
        E[Logging - app.log, stdout]
    end

    A --> B
    B -->|Error| D
    C -->|Error| D
    D --> E
    D -->|Return Error Response| A
```

---

## 6. File Processing (Batch Upload)

```mermaid
flowchart TD
    A[Client Uploads File] --> B[FastAPI Router]
    B --> C[FileProcessingService]
    C --> D[Check File Type - CSV/JSON]
    D -->|Invalid| E[Return 400 Error]
    D --> F[Extract Names]
    F -->|Missing Column/Field| E
    F --> G[Return List of Names]
```

---

## 7. Configuration & Environment

```mermaid
flowchart TD
    A[.env / .env.example] --> B[app/config.py - Settings]
    B --> C[All Backend Components]
    C --> D[Read config values at startup]
```

---

## 8. Logging Flow

```mermaid

flowchart TD
    A[API/Service/Exception] --> B[Logger]
    B --> C[app.log file]
    B --> D[stdout]
    
```

---

## 9. Response Models

**Single Match:**
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

**Batch Match:**
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
    },
    "error": null
  }
]
```

---

**Legend:**
- **Client**: Frontend or API consumer
- **FastAPI Router**: Endpoint handler
- **Service Layer**: Business logic (MatchingService, FileProcessingService)
- **FuzzyMatcher**: Core matching logic
- **Logger**: Centralized logging
- **Config**: Environment and settings
