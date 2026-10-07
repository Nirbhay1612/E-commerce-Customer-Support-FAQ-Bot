"""
Tests for the RAG chain.

Covers:
- FAQ document formatting
- Empty document handling
- Document metadata handling
- Multiple document formatting
- Chat history formatting
- RAG input validation
"""

import pytest
from typing import Any, cast
from langchain_core.documents import Document

from src.rag.rag_chain import (
    format_chat_history,
    format_docs,
    get_rag_response,
)


# -------------------------------------------------------------------
# format_docs() Tests
# -------------------------------------------------------------------

def test_format_empty_documents():
    result = format_docs([])

    assert "No relevant FAQ information" in result


def test_format_documents():
    documents = [
        Document(
            page_content="Return policy: 30 days."
        )
    ]

    result = format_docs(documents)

    assert "FAQ 1" in result
    assert "Return policy" in result


def test_format_document_with_category():
    documents = [
        Document(
            page_content="Returns are accepted within 30 days.",
            metadata={"category": "Returns"},
        )
    ]

    result = format_docs(documents)

    assert "FAQ 1" in result
    assert "Category: Returns" in result
    assert "Returns are accepted" in result


def test_format_multiple_documents():
    documents = [
        Document(
            page_content="Return policy: 30 days."
        ),
        Document(
            page_content="Delivery usually takes 3-5 days."
        ),
    ]

    result = format_docs(documents)

    assert "FAQ 1" in result
    assert "FAQ 2" in result
    assert "Return policy" in result
    assert "Delivery usually takes" in result


def test_format_empty_document_content():
    documents = [
        Document(page_content=""),
        Document(page_content="Valid FAQ content."),
    ]

    result = format_docs(documents)

    assert "Valid FAQ content." in result
    assert "No relevant FAQ information" not in result


def test_format_only_empty_documents():
    documents = [
        Document(page_content=""),
        Document(page_content="   "),
    ]

    result = format_docs(documents)

    assert "No relevant FAQ information" in result


def test_format_docs_ignores_invalid_objects():
    documents = [
        "not a document",
        Document(page_content="Valid FAQ content."),
    ]

    result = format_docs(documents)

    assert "Valid FAQ content." in result
    assert "not a document" not in result


# -------------------------------------------------------------------
# format_chat_history() Tests
# -------------------------------------------------------------------

def test_format_empty_chat_history():
    result = format_chat_history([])

    assert result == "No previous conversation."


def test_format_none_chat_history():
    result = format_chat_history(None)

    assert result == "No previous conversation."


def test_format_dict_chat_history():
    history = [
        {
            "role": "user",
            "content": "Where is my order?",
        },
        {
            "role": "assistant",
            "content": "Please provide your order details.",
        },
    ]

    result = format_chat_history(history)

    assert "Customer: Where is my order?" in result
    assert "Assistant: Please provide your order details." in result


def test_format_langchain_chat_history():
    from langchain_core.messages import (
        AIMessage,
        HumanMessage,
    )

    history = [
        HumanMessage(content="What is your return policy?"),
        AIMessage(content="Returns are accepted within 30 days."),
    ]

    result = format_chat_history(history)

    assert "Customer: What is your return policy?" in result
    assert "Assistant: Returns are accepted within 30 days." in result


def test_format_chat_history_ignores_empty_messages():
    history = [
        {
            "role": "user",
            "content": "",
        },
        {
            "role": "assistant",
            "content": "Valid response.",
        },
    ]

    result = format_chat_history(history)

    assert "Valid response." in result
    assert "Customer:" not in result


# -------------------------------------------------------------------
# get_rag_response() Input Validation
# -------------------------------------------------------------------

def test_get_rag_response_rejects_empty_question():
    with pytest.raises(
        ValueError,
        match="Question cannot be empty",
    ):
        get_rag_response("")


def test_get_rag_response_rejects_whitespace_question():
    with pytest.raises(
        ValueError,
        match="Question cannot be empty",
    ):
        get_rag_response("   ")


def test_get_rag_response_rejects_non_string_question():
    with pytest.raises(
        ValueError,
        match="Question must be a string",
    ):
        get_rag_response(cast(Any, 12345))


def test_get_rag_response_rejects_invalid_chat_history():
    with pytest.raises(
        ValueError,
        match="Chat history must be a list",
    ):
        get_rag_response(
            "What is your return policy?",
            chat_history=cast(Any, ("invalid history",)),
        )