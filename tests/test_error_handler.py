"""
Tests for the centralized error handler.

Covers:
- Error classification
- Safe user-facing error responses
- Unknown error handling
- Sensitive information protection
"""

import pytest

from src.utils.error_handler import (
    get_error_response,
    get_error_type,
    handle_error,
)


# -------------------------------------------------------------------
# Error Classification Tests
# -------------------------------------------------------------------

def test_timeout_error():
    error = Exception("Request timed out")

    assert get_error_type(error) == "timeout"


def test_timeout_keyword_error():
    error = Exception("The request exceeded the deadline")

    assert get_error_type(error) == "timeout"


def test_rate_limit_error():
    error = Exception("429 Too Many Requests")

    assert get_error_type(error) == "rate_limit"


def test_authentication_error():
    error = Exception("401 Unauthorized")

    assert get_error_type(error) == "authentication"


def test_invalid_api_key_error():
    error = Exception("Invalid API key")

    assert get_error_type(error) == "authentication"


def test_permission_error():
    error = Exception("403 Forbidden")

    assert get_error_type(error) == "permission"


def test_connection_error():
    error = Exception("Connection error")

    assert get_error_type(error) == "connection"


def test_network_error():
    error = Exception("Network connection failed")

    assert get_error_type(error) == "connection"


def test_retrieval_error():
    error = Exception("Chroma vectorstore retrieval failed")

    assert get_error_type(error) == "retrieval"


def test_embedding_error():
    error = Exception("Sentence-transformers embedding failed")

    assert get_error_type(error) == "embedding"


def test_llm_error():
    error = Exception("Groq LLM failed")

    assert get_error_type(error) == "llm"


def test_unknown_error():
    error = Exception("Something unexpected happened")

    assert get_error_type(error) == "unknown"


# -------------------------------------------------------------------
# Error Response Tests
# -------------------------------------------------------------------

@pytest.mark.parametrize(
    "error_message",
    [
        "Request timed out",
        "429 Too Many Requests",
        "401 Unauthorized",
        "Connection error",
        "403 Forbidden",
        "Chroma vectorstore failed",
        "Embedding model failed",
        "Groq LLM failed",
        "Something unexpected happened",
    ],
)
def test_error_response_returns_string(error_message):
    error = Exception(error_message)

    response = get_error_response(error)

    assert isinstance(response, str)
    assert response.strip()


def test_error_response_is_safe():
    error = Exception(
        "API key SECRET_PASSWORD 12345"
    )

    response = get_error_response(error)

    assert isinstance(response, str)
    assert "SECRET_PASSWORD" not in response
    assert "12345" not in response


def test_error_response_does_not_expose_api_key():
    error = Exception(
        "Authentication failed: sk-secret-api-key-12345"
    )

    response = get_error_response(error)

    assert "sk-secret-api-key-12345" not in response


# -------------------------------------------------------------------
# handle_error() Tests
# -------------------------------------------------------------------

def test_handle_error_returns_safe_response():
    error = Exception("Something unexpected happened")

    response = handle_error(error)

    assert isinstance(response, str)
    assert response.strip()


def test_handle_error_matches_error_response():
    error = Exception("Request timed out")

    assert handle_error(error) == get_error_response(error)


def test_handle_error_does_not_expose_internal_error():
    error = Exception(
        "Groq API failed with SECRET_TOKEN_123"
    )

    response = handle_error(error)

    assert "SECRET_TOKEN_123" not in response