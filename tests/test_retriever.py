"""
Tests for the FAQ retriever.

Covers:
- FAQ document retrieval
- Retrieved document validation
- Query validation
- Top-k validation
- Empty query handling
"""
from typing import Any, cast
import pytest
from langchain_core.documents import Document

from src.rag.retriever import (
    DEFAULT_TOP_K,
    MAX_TOP_K,
    retrieve_faq,
    validate_top_k,
)


# -------------------------------------------------------------------
# Basic Retrieval Tests
# -------------------------------------------------------------------

def test_retrieve_faq():
    results = retrieve_faq(
        "What is the return policy?"
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_retrieved_documents_are_valid():
    results = retrieve_faq(
        "How long does delivery take?"
    )

    assert results

    for document in results:
        assert isinstance(document, Document)
        assert document.page_content
        assert isinstance(document.page_content, str)
        assert document.page_content.strip()


def test_retrieved_documents_have_metadata():
    results = retrieve_faq(
        "What payment methods are supported?"
    )

    assert results

    for document in results:
        assert isinstance(document.metadata, dict)


# -------------------------------------------------------------------
# Top-K Tests
# -------------------------------------------------------------------

def test_default_top_k():
    results = retrieve_faq(
        "What is the return policy?"
    )

    assert len(results) <= DEFAULT_TOP_K


def test_custom_top_k():
    results = retrieve_faq(
        "What is the return policy?",
        k=2,
    )

    assert isinstance(results, list)
    assert len(results) <= 2


def test_validate_top_k_accepts_valid_value():
    assert validate_top_k(3) == 3


def test_validate_top_k_rejects_zero():
    with pytest.raises(ValueError, match="at least 1"):
        validate_top_k(0)


def test_validate_top_k_rejects_negative_value():
    with pytest.raises(ValueError, match="at least 1"):
        validate_top_k(-1)


def test_validate_top_k_rejects_value_above_maximum():
    with pytest.raises(
        ValueError,
        match=f"greater than {MAX_TOP_K}",
    ):
        validate_top_k(MAX_TOP_K + 1)


def test_validate_top_k_rejects_non_integer():
    with pytest.raises(ValueError, match="integer"):
        validate_top_k(cast(Any,"3"))


def test_validate_top_k_rejects_boolean():
    with pytest.raises(ValueError, match="integer"):
        validate_top_k(True)


# -------------------------------------------------------------------
# Query Validation Tests
# -------------------------------------------------------------------

def test_empty_query_raises_error():
    with pytest.raises(
        ValueError,
        match="Query cannot be empty",
    ):
        retrieve_faq("")


def test_whitespace_query_raises_error():
    with pytest.raises(
        ValueError,
        match="Query cannot be empty",
    ):
        retrieve_faq("   ")


def test_none_query_raises_error():
    with pytest.raises(
        ValueError,
        match="Query must be a string",
    ):
        retrieve_faq(cast(Any, None))


def test_non_string_query_raises_error():
    with pytest.raises(
        ValueError,
        match="Query must be a string",
    ):
        retrieve_faq(cast(Any, 12345))


# -------------------------------------------------------------------
# Retrieval Result Quality Tests
# -------------------------------------------------------------------

def test_retrieval_returns_only_documents():
    results = retrieve_faq(
        "How can I return an item?"
    )

    assert results

    for document in results:
        assert isinstance(document, Document)


def test_retrieval_result_count_does_not_exceed_k():
    k = 3

    results = retrieve_faq(
        "How does shipping work?",
        k=k,
    )

    assert len(results) <= k