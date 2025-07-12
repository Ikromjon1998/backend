# C4 Documentation: Fuzzy Entity Matching API

## 1. System Context Diagram

```mermaid
C4Context
    title System Context diagram for Fuzzy Entity Matching API
    Person(user, "User", "Data engineer, developer, or system integrating entity matching")
    System_Boundary(fem_api, "Fuzzy Entity Matching API") {
        System(fem_api_core, "Fuzzy Entity Matching API", "REST API for fuzzy entity matching")
    }
    System_Ext(system1, "External Data Source", "CRM, ERP, or other data provider")
    System_Ext(system2, "Frontend App", "Web or mobile client consuming the API")
    Rel(user, fem_api_core, "Uses", "HTTP/REST")
    Rel(system1, fem_api_core, "Provides entity data", "CSV/JSON upload")
    Rel(fem_api_core, system2, "Returns match results", "JSON/REST")
```

**Explanation:**
- The Fuzzy Entity Matching API is used by data engineers, developers, or other systems.
- It receives entity data from external sources (e.g., CRM, ERP) and provides results to frontend apps or other consumers.

---

## 2. Container Diagram

```mermaid
C4Container
    title Container diagram for Fuzzy Entity Matching API
    System_Boundary(fem_api, "Fuzzy Entity Matching API") {
        Container(web_api, "FastAPI Application", "Python/FastAPI", "Exposes REST endpoints for matching and batch processing")
        Container(matcher, "FuzzyMatcher Service", "Python", "Implements fuzzy matching logic (TF-IDF, Levenshtein, token set)")
        Container(preprocessor, "Preprocessor", "Python", "Normalizes and standardizes entity names")
        Container(config, "Config Module", "Python", "Centralizes configuration and canonical entities")
        Container(models, "Models Module", "Python/Pydantic", "Defines request/response schemas")
        Container(services, "Services Module", "Python", "Business logic for file processing and matching")
        Container(routers, "Routers Module", "Python/FastAPI", "Organizes API endpoints")
    }
    Rel(web_api, matcher, "Uses")
    Rel(web_api, preprocessor, "Uses")
    Rel(web_api, config, "Reads config")
    Rel(web_api, models, "Uses models")
    Rel(web_api, services, "Uses services")
    Rel(web_api, routers, "Includes routers")
    Rel(matcher, preprocessor, "Uses for normalization")
```

**Explanation:**
- The FastAPI application is the main entry point, exposing REST endpoints.
- Business logic is separated into services, with dedicated modules for configuration, models, and routing.
- The matcher and preprocessor are core components for fuzzy matching and normalization.

---

## 3. Component & Code Diagrams (Optional)

For further detail, you can add C4 Component diagrams for each container, or sequence diagrams for request flows. Let me know if you want to visualize these as well!

---

**This C4 documentation provides a high-level architectural overview of the Fuzzy Entity Matching API, supporting onboarding, review, and future development.** 