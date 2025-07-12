"""
Logging configuration for the Fuzzy Entity Matching API.
"""
import logging
import sys
from typing import Dict, Any


def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup logging configuration for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

    # Set specific loggers
    loggers = {
        'uvicorn': logging.INFO,
        'fastapi': logging.INFO,
        'app': logging.DEBUG if log_level.upper() == 'DEBUG' else logging.INFO
    }

    for logger_name, level in loggers.items():
        logging.getLogger(logger_name).setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


# Logging configuration for different environments
LOGGING_CONFIGS: Dict[str, Dict[str, Any]] = {
    'development': {
        'level': 'DEBUG',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },
    'production': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },
    'testing': {
        'level': 'WARNING',
        'format': '%(levelname)s - %(message)s'
    }
}
