"""
Fallback Response System

Responsible for:
- Providing safe fallback responses
- Detecting basic user intent when the normal
  LLM/RAG pipeline cannot respond

Fallback responses must not invent:
- Business policies
- Prices
- Delivery dates
- Refund timelines
- Real-time order information
"""
import re
from typing import Final
from typing import Optional


# -------------------------------------------------------------------
# Fallback Responses
# -------------------------------------------------------------------

FALLBACK_RESPONSES: Final[dict[str, str]] = {
    "default": (
        "I'm sorry, I don't have enough information to answer "
        "that accurately. Please try rephrasing your question."
    ),

    "api_error": (
        "I'm currently experiencing a technical issue. "
        "Please try again shortly."
    ),

    "timeout": (
        "Your request is taking longer than expected. "
        "Please try again in a moment."
    ),

    "empty_response": (
        "I couldn't generate a response just now. "
        "Please rephrase your question and try again."
    ),

    "order_status": (
        "I don't have access to live order information. "
        "Please use the official ShopEase order-tracking system "
        "or contact customer support for your current order status."
    ),

    "return_refund": (
        "I can help explain ShopEase's return, refund, or exchange "
        "information when it is available in the support knowledge base."
    ),

    "shipping": (
        "I can help with ShopEase shipping and delivery information "
        "when it is available in the support knowledge base."
    ),

    "payment": (
        "I can help with general ShopEase payment information. "
        "For account-specific payment issues, please use the secure "
        "ShopEase support channel. Never share your full card number, "
        "CVV, password, or OTP."
    ),

    "greeting": (
        "Hello! Welcome to ShopEase Support. "
        "How can I help you today?"
    ),

    "thanks": (
        "You're welcome! Is there anything else I can help "
        "you with?"
    ),

    "escalate": (
        "I understand you'd like additional support. "
        "Please contact the appropriate ShopEase support channel "
        "for assistance from a human agent."
    ),
}


# -------------------------------------------------------------------
# Fallback Intent Keywords
# -------------------------------------------------------------------

INTENT_KEYWORDS: Final[dict[str, tuple[str, ...]]] = {
    "escalate": (
        "talk to human",
        "talk to someone",
        "speak to someone",
        "human agent",
        "human",
        "agent",
        "representative",
        "customer care",
        "customer service",
    ),

    "greeting": (
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    ),

    "thanks": (
        "thank you",
        "thanks",
        "thx",
    ),

    "return_refund": (
        "return",
        "refund",
        "exchange",
        "replace",
    ),

    "order_status": (
        "order status",
        "where is my order",
        "track my order",
        "order tracking",
        "tracking",
    ),

    "shipping": (
        "shipping",
        "delivery",
        "courier",
        "arrive",
        "delayed",
    ),

    "payment": (
        "payment",
        "paid",
        "card",
        "upi",
        "transaction",
        "billing",
    ),
}


# -------------------------------------------------------------------
# Get Fallback
# -------------------------------------------------------------------

def get_fallback(key:Optional[str] = "default") -> str:
    """
    Return a predefined fallback response.

    Args:
        key:
            Fallback response identifier.

    Returns:
        User-friendly fallback response.
    """

    if not isinstance(key, str):
        return FALLBACK_RESPONSES["default"]

    normalized_key = key.strip().lower()

    return FALLBACK_RESPONSES.get(
        normalized_key,
        FALLBACK_RESPONSES["default"],
    )


# -------------------------------------------------------------------
# Intent Detection
# -------------------------------------------------------------------

def detect_fallback_intent(
    user_message: str | None
) -> str:
    """
    Detect a basic user intent using predefined keywords.

    This function should be used only when the normal
    LLM/RAG pipeline cannot provide a suitable response.

    Args:
        user_message:
            User's message.

    Returns:
        Detected fallback intent.
    """

    if not isinstance(user_message, str):
        return "default"

    message = " ".join(
        user_message.lower().split()
    )

    if not message:
        return "default"

    priority_order = (
        "escalate",
        "greeting",
        "thanks",
        "return_refund",
        "order_status",
        "shipping",
        "payment",
    )

    for intent in priority_order:

        keywords = INTENT_KEYWORDS[intent]

        for keyword in keywords :
            pattern=rf"\b{re.escape(keyword)}\b"

            if re.search(pattern, message):
                return intent

    return "default"