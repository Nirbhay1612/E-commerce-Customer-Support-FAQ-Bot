"""
Tests for the response handler.

Covers:
- Normal string responses
- LangChain message responses
- Empty responses
- Whitespace cleanup
- Response length limiting
- Final response validation
"""

from langchain_core.messages import AIMessage
import pytest

from src.chatbot.response_handler import (
    MAX_RESPONSE_LENGTH,
    clean_response,
    handle_response,
    is_valid_response,
)


# -------------------------------------------------------------------
# clean_response() tests
# -------------------------------------------------------------------

def test_clean_response_with_normal_string():
    response = "Hello! How can I help you?"

    result = clean_response(response)

    assert result == "Hello! How can I help you?"


def test_clean_response_with_whitespace():
    response = "   Hello! How can I help you?   "

    result = clean_response(response)

    assert result == "Hello! How can I help you?"


def test_clean_response_with_trailing_spaces():
    response = "Hello!   \nHow can I help you?   "

    result = clean_response(response)

    assert result == "Hello!\nHow can I help you?"


def test_clean_response_with_none():
    result = clean_response(None)

    assert result == ""


def test_clean_response_with_empty_string():
    result = clean_response("")

    assert result == ""


def test_clean_response_with_whitespace_only():
    result = clean_response("     \n   ")

    assert result == ""


def test_clean_response_with_ai_message():
    response = AIMessage(
        content="Your order has been shipped."
    )

    result = clean_response(response)

    assert result == "Your order has been shipped."


def test_clean_response_with_other_object():
    response = 12345

    result = clean_response(response)

    assert result == "12345"


# -------------------------------------------------------------------
# Response length tests
# -------------------------------------------------------------------

def test_clean_response_respects_max_length():
    response = "word " * 1000

    result = clean_response(response)

    assert len(result) <= MAX_RESPONSE_LENGTH
    assert result.endswith("...")


def test_clean_response_does_not_truncate_short_response():
    response = "This is a short response."

    result = clean_response(response)

    assert result == response
    assert not result.endswith("...")


# -------------------------------------------------------------------
# is_valid_response() tests
# -------------------------------------------------------------------

def test_is_valid_response_with_valid_text():
    response = "Your order is on the way."

    assert is_valid_response(response) is True


def test_is_valid_response_with_empty_response():
    response = ""

    assert is_valid_response(response) is False


def test_is_valid_response_with_none():
    assert is_valid_response(None) is False


def test_is_valid_response_with_ai_message():
    response = AIMessage(
        content="Your refund has been processed."
    )

    assert is_valid_response(response) is True


# -------------------------------------------------------------------
# handle_response() tests
# -------------------------------------------------------------------

def test_handle_response_returns_clean_response():
    response = "   Your order is confirmed.   "

    result = handle_response(response)

    assert result == "Your order is confirmed."


def test_handle_response_accepts_ai_message():
    response = AIMessage(
        content="Your refund will be processed."
    )

    result = handle_response(response)

    assert result == "Your refund will be processed."


def test_handle_response_raises_for_empty_response():
    with pytest.raises(ValueError, match="empty response"):
        handle_response("")


def test_handle_response_raises_for_none():
    with pytest.raises(ValueError, match="empty response"):
        handle_response(None)


def test_handle_response_raises_for_whitespace():
    with pytest.raises(ValueError, match="empty response"):
        handle_response("   ")