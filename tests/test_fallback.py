"""
Tests for the fallback response system.

Covers:
- Fallback response retrieval
- Intent detection
- Empty and invalid input handling
- Supported fallback intents
- Unknown intent handling
"""

import pytest

from src.utils.fallback import (
    FALLBACK_RESPONSES,
    detect_fallback_intent,
    get_fallback,
)


# -------------------------------------------------------------------
# get_fallback() Tests
# -------------------------------------------------------------------

def test_default_fallback():
    response = get_fallback()

    assert isinstance(response, str)
    assert response.strip()


@pytest.mark.parametrize(
    "fallback_key",
    [
        "default",
        "api_error",
        "timeout",
        "empty_response",
        "order_status",
        "return_refund",
        "shipping",
        "payment",
        "greeting",
        "thanks",
        "escalate",
    ],
)
def test_all_fallback_responses_exist(fallback_key):
    response = get_fallback(fallback_key)

    assert isinstance(response, str)
    assert response.strip()
    assert response == FALLBACK_RESPONSES[fallback_key]


def test_unknown_fallback_key_returns_default():
    response = get_fallback("unknown_key")

    assert response == FALLBACK_RESPONSES["default"]


def test_fallback_key_is_case_insensitive():
    response = get_fallback("GREETING")

    assert response == FALLBACK_RESPONSES["greeting"]


def test_fallback_key_ignores_whitespace():
    response = get_fallback("  greeting  ")

    assert response == FALLBACK_RESPONSES["greeting"]


def test_invalid_fallback_key_returns_default():
    assert get_fallback(None) == FALLBACK_RESPONSES["default"]


# -------------------------------------------------------------------
# Intent Detection Tests
# -------------------------------------------------------------------

def test_greeting_intent():
    intent = detect_fallback_intent("Hello")

    assert intent == "greeting"


def test_thanks_intent():
    intent = detect_fallback_intent("Thank you")

    assert intent == "thanks"


def test_return_refund_intent():
    intent = detect_fallback_intent(
        "I want to return my product"
    )

    assert intent == "return_refund"


def test_order_status_intent():
    intent = detect_fallback_intent(
        "Where is my order?"
    )

    assert intent == "order_status"


def test_shipping_intent():
    intent = detect_fallback_intent(
        "My delivery is delayed"
    )

    assert intent == "shipping"


def test_payment_intent():
    intent = detect_fallback_intent(
        "I have a payment problem"
    )

    assert intent == "payment"


def test_escalation_intent():
    intent = detect_fallback_intent(
        "I want to speak to a human agent"
    )

    assert intent == "escalate"


# -------------------------------------------------------------------
# Input Normalization Tests
# -------------------------------------------------------------------

def test_empty_message():
    intent = detect_fallback_intent("")

    assert intent == "default"


def test_whitespace_message():
    intent = detect_fallback_intent("   ")

    assert intent == "default"


def test_none_message():
    intent = detect_fallback_intent(None)

    assert intent == "default"


def test_unknown_message():
    intent = detect_fallback_intent(
        "Tell me something completely random"
    )

    assert intent == "default"


def test_intent_detection_is_case_insensitive():
    intent = detect_fallback_intent(
        "I WANT TO SPEAK TO A HUMAN AGENT"
    )

    assert intent == "escalate"


def test_intent_detection_handles_extra_whitespace():
    intent = detect_fallback_intent(
        "   Where    is    my    order?   "
    )

    assert intent == "order_status"


# -------------------------------------------------------------------
# Priority Tests
# -------------------------------------------------------------------

def test_escalation_has_priority():
    intent = detect_fallback_intent(
        "I have a payment problem, talk to a human agent"
    )

    assert intent == "escalate"