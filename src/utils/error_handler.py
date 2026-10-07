"""
Centralized Error Handler

Responsible for:
- Categorizing application errors
- Converting technical errors into safe user-facing messages
- Preventing raw exceptions from reaching users

Logging is handled separately by the application logger.
"""

from typing import Any

from src.utils.fallback import get_fallback


# -------------------------------------------------------------------
# Error Classification
# -------------------------------------------------------------------

def get_error_type(error: Any) -> str:
    """
    Identify the category of an application error.

    Args:
        error:
            Exception or error object.

    Returns:
        Error category name.
    """

    error_message = str(error).lower()

    # ---------------------------------------------------------------
    # Timeout
    # ---------------------------------------------------------------

    if any(
        keyword in error_message
        for keyword in (
            "timeout",
            "timed out",
            "deadline exceeded",
            "exceeded the deadline"
        )
    ):
        return "timeout"

    # ---------------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------------

    if any(
        keyword in error_message
        for keyword in (
            "401",
            "unauthorized",
            "authentication",
            "invalid api key",
        )
    ):
        return "authentication"

    # ---------------------------------------------------------------
    # Permission
    # ---------------------------------------------------------------

    if any(
        keyword in error_message
        for keyword in (
            "403",
            "forbidden",
            "permission denied",
        )
    ):
        return "permission"

    # ---------------------------------------------------------------
    # Rate Limit
    # ---------------------------------------------------------------

    if any(
        keyword in error_message
        for keyword in (
            "429",
            "rate limit",
            "too many requests",
        )
    ):
        return "rate_limit"

    # ---------------------------------------------------------------
    # Connection / Network
    # ---------------------------------------------------------------

    if any(
        keyword in error_message
        for keyword in (
            "connection refused",
            "connection reset",
            "connection",
            "network",
            "connect error",
        )
    ):
        return "connection"

    # ---------------------------------------------------------------
    # Vector Store / Retrieval
    # ---------------------------------------------------------------

    if any(
        keyword in error_message
        for keyword in (
            "chroma",
            "vectorstore",
            "vector store",
            "retriever",
            "retrieval",
        )
    ):
        return "retrieval"

    # ---------------------------------------------------------------
    # Embeddings
    # ---------------------------------------------------------------

    if any(
        keyword in error_message
        for keyword in (
            "embedding",
            "embeddings",
            "sentence-transformers",
        )
    ):
        return "embedding"

    # ---------------------------------------------------------------
    # LLM / Model
    # ---------------------------------------------------------------

    if any(
        keyword in error_message
        for keyword in (
            "groq",
            "chatgroq",
            "llm",
            "model",
        )
    ):
        return "llm"

    # ---------------------------------------------------------------
    # Unknown
    # ---------------------------------------------------------------

    return "unknown"


# -------------------------------------------------------------------
# User-Facing Error Messages
# -------------------------------------------------------------------

ERROR_RESPONSES: dict[str, str] = {
    "timeout": (
        "Your request is taking longer than expected. "
        "Please try again in a moment."
    ),

    "authentication": (
        "The support service is currently unavailable. "
        "Please try again later."
    ),

    "permission": (
        "The support service cannot process your request "
        "right now. Please try again later."
    ),

    "rate_limit": (
        "The support service is temporarily busy. "
        "Please try again shortly."
    ),

    "connection": (
        "I'm having trouble connecting to the support service. "
        "Please try again shortly."
    ),

    "retrieval": (
        "I'm having trouble accessing the support information "
        "right now. Please try again shortly."
    ),

    "embedding": (
        "The support knowledge system is temporarily unavailable. "
        "Please try again later."
    ),

    "llm": (
        "I'm currently unable to generate a response. "
        "Please try again shortly."
    ),

    "unknown": (
        "I'm sorry, something went wrong while processing "
        "your request. Please try again shortly."
    ),
}


# -------------------------------------------------------------------
# Safe Error Response
# -------------------------------------------------------------------

def get_error_response(error: Any) -> str:
    """
    Convert a technical error into a safe user-facing response.

    Technical details are intentionally not exposed.

    Args:
        error:
            Exception or error object.

    Returns:
        Safe response for the user.
    """

    error_type = get_error_type(error)

    return ERROR_RESPONSES.get(
        error_type,
        get_fallback("api_error"),
    )


# -------------------------------------------------------------------
# Main Error Handler
# -------------------------------------------------------------------

def handle_error(error: Any) -> str:
    """
    Main application error handler.

    Args:
        error:
            Exception or error object.

    Returns:
        Safe user-facing error message.
    """

    return get_error_response(error)