# C4 Documentation: Fuzzy Entity Matching API

## Context

This API provides fuzzy entity matching for German company names and legal entities. It is built with FastAPI and uses a modular, maintainable architecture with strong configuration and logging support.

## Containers

- **FastAPI Application**: Main API server
- **Configuration**: Managed via `app/config.py` and `.env`/`.env.example` files
- **Logging**: Centralized in `app/logging_config.py`, configurable via `LOG_LEVEL` in `.env`
- **Business Logic**: `app/services.py` and `app/matcher.py`
- **API Models**: `app/models.py`
- **Preprocessing**: `app/preprocessor.py`
- **Routing**: `app/routers.py`

## Configuration

- All environment variables are documented in `.env.example`.
- The `.env` file is loaded automatically; extra fields are ignored due to the config setting in `app/config.py`.
- **LOG_LEVEL** controls the logging verbosity (e.g., INFO, DEBUG, WARNING).
- See `app/logging_config.py` for logging setup details.

## Logging

- Logging is configured in `app/logging_config.py`.
- Logs are written to both stdout and `app.log`.
- The log level is set via the `LOG_LEVEL` environment variable.
- All major events, errors, and service initializations are logged.

## Deployment

- Copy `.env.example` to `.env` and adjust as needed.
- Run with Uvicorn or Docker as described in the README.

## Extensibility

- Add new configuration variables to `.env.example` and `app/config.py`.
- Add new logging channels or handlers in `app/logging_config.py`.
- All new features should be documented in the README and C4 docs. 