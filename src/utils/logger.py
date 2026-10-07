"""
Application Logger

Responsible for:
- Centralized application logging
- Recording errors and warnings
- Providing consistent log formatting
- Keeping technical details out of user-facing responses
"""

import logging
from pathlib import Path


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_DIRECTORY = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIRECTORY / "app.log"

LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


# -------------------------------------------------------------------
# Logger Configuration
# -------------------------------------------------------------------

LOGGER_NAME = "shopease"

logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.INFO)


# Prevent duplicate handlers when Streamlit reloads the application
if not logger.handlers:

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    # Console handler
    console_handler = logging.StreamHandler()

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------

def log_info(message: str) -> None:
    """
    Log an informational message.
    """

    logger.info(message)


def log_warning(message: str) -> None:
    """
    Log a warning message.
    """

    logger.warning(message)


def log_error(
    message: str,
    error: Exception | None = None,
) -> None:
    """
    Log an error message.

    Args:
        message: Description of the error.
        error: Optional exception object.
    """

    if error is not None:
        logger.error(
            "%s | %s: %s",
            message,
            type(error).__name__,
            error,
            exc_info=True,
        )
    else:
        logger.error(message)


def log_debug(message: str) -> None:
    """
    Log a debug message.

    Debug messages are hidden unless the logger level
    is changed to DEBUG.
    """

    logger.debug(message)