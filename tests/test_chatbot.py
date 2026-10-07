"""
Tests for the main chatbot orchestration layer.

Covers:
- User message validation
- Whitespace handling
- Invalid input handling
- Conversation history validation
"""

import pytest
from typing import Any,cast
from langchain_core.messages import AIMessage, HumanMessage

from src.chatbot.chatbot import (
    MAX_HISTORY_MESSAGES,
    normalize_chat_history,
    validate_user_message,
)


# -------------------------------------------------------------------
# validate_user_message() Tests
# -------------------------------------------------------------------

def test_valid_message():
    result = validate_user_message(
        "What is your return policy?"
    )

    assert result == "What is your return policy?"


def test_message_is_trimmed():
    result = validate_user_message(
        "   Hello   "
    )

    assert result == "Hello"


def test_empty_message():
    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        validate_user_message("")


def test_whitespace_message():
    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        validate_user_message("   ")


def test_non_string_message():
    with pytest.raises(
        ValueError,
        match="must be a string",
    ):
        validate_user_message(None)


def test_numeric_message():
    with pytest.raises(
        ValueError,
        match="must be a string",
    ):
        validate_user_message(cast(Any, 12345))


# -------------------------------------------------------------------
# normalize_chat_history() Tests
# -------------------------------------------------------------------

def test_empty_chat_history():
    result = normalize_chat_history([])

    assert result == []


def test_none_chat_history():
    result = normalize_chat_history(None)

    assert result == []


def test_valid_chat_history():
    history = [
        HumanMessage(content="Hello"),
        AIMessage(content="Hi! How can I help?"),
    ]

    result = normalize_chat_history(history)

    assert len(result) == 2
    assert isinstance(result[0], HumanMessage)
    assert isinstance(result[1], AIMessage)


def test_chat_history_keeps_only_valid_messages():
    history = [
        HumanMessage(content="Hello"),
        "invalid message",
        AIMessage(content="How can I help?"),
    ]

    result = normalize_chat_history(history)

    assert len(result) == 2
    assert all(
        isinstance(message, (HumanMessage, AIMessage))
        for message in result
    )


def test_chat_history_is_limited():
    history = [
        HumanMessage(content=f"Message {index}")
        for index in range(MAX_HISTORY_MESSAGES + 5)
    ]

    result = normalize_chat_history(cast(Any, history))

    assert len(result) == MAX_HISTORY_MESSAGES


def test_chat_history_keeps_most_recent_messages():
    history = [
        HumanMessage(content=f"Message {index}")
        for index in range(MAX_HISTORY_MESSAGES + 2)
    ]

    result = normalize_chat_history(cast(Any, history))

    assert result[-1].content == f"Message {MAX_HISTORY_MESSAGES + 1}"


def test_invalid_chat_history_type():
    with pytest.raises(
        ValueError,
        match="Chat history must be a list",
    ):
        normalize_chat_history(cast(Any, "invalid history"))