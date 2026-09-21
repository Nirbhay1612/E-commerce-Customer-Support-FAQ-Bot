"""
Fallback responses for the e-commerce customer support chatbot.
Used when LLM fails, times out, or returns empty/invalid response.
"""

FALLBACK_RESPONSES = {
    # General errors
    "default": (
        "I'm sorry, I'm having a little trouble right now. "
        "Could you please try again in a moment? "
        "If the issue continues, I can connect you with a human agent."
    ),
    
    "api_error": (
        "I'm currently experiencing a technical issue. "
        "Please try again shortly, or I can transfer you to a support agent for immediate help."
    ),
    
    "timeout": (
        "It's taking longer than expected to process your request. "
        "Please try again, or let me know if you'd like to speak with a human agent."
    ),
    
    "empty_response": (
        "I apologize, I couldn't generate a proper response just now. "
        "Could you rephrase your question? I'm here to help!"
    ),
    
    # Common customer intents (simple keyword-based fallback)
    "order_status": (
        "I'd be happy to help you check your order status. "
        "Could you please share your order number or the email used for the order?"
    ),
    
    "return_refund": (
        "I can help you with returns and refunds. "
        "Our return window is 30 days from delivery. "
        "Could you please share your order number so I can assist further?"
    ),
    
    "shipping": (
        "For shipping queries, I need a bit more information. "
        "Could you share your order number? Standard delivery usually takes 3–7 business days."
    ),
    
    "payment": (
        "I'm here to help with payment-related questions. "
        "For security reasons, please never share full card details. "
        "Could you describe the issue you're facing?"
    ),
    
    "greeting": (
        "Hello! Welcome to our store support. "
        "How can I assist you today? I can help with orders, returns, shipping, and more."
    ),
    
    "thanks": (
        "You're welcome! Is there anything else I can help you with today?"
    ),
    
    "escalate": (
        "I understand this needs more personalized attention. "
        "Let me connect you with a human support agent. "
        "Please hold on while I transfer your chat."
    ),
}


def get_fallback(key: str = "default") -> str:
    """Return a fallback response by key. Defaults to 'default' if key not found."""
    return FALLBACK_RESPONSES.get(key, FALLBACK_RESPONSES["default"])


def detect_fallback_intent(user_message: str) -> str:
    """
    Very simple keyword-based intent detection for fallback.
    Used only when LLM fails.
    """
    msg = user_message.lower().strip()

    if any(w in msg for w in ["hi", "hello", "hey", "good morning", "good evening"]):
        return "greeting"
    
    if any(w in msg for w in ["thank", "thanks", "thx"]):
        return "thanks"
    
    if any(w in msg for w in ["order", "track", "status", "where is my", "delivery status"]):
        return "order_status"
    
    if any(w in msg for w in ["return", "refund", "exchange", "replace"]):
        return "return_refund"
    
    if any(w in msg for w in ["shipping", "delivery", "courier", "when will it arrive"]):
        return "shipping"
    
    if any(w in msg for w in ["payment", "paid", "card", "upi", "transaction", "billing"]):
        return "payment"
    
    if any(w in msg for w in ["agent", "human", "person", "speak to", "talk to someone", "representative"]):
        return "escalate"
    
    return "default"

def handle_api_error(error):
    error_message = str(error).lower()

    if "401" in error_message or "authentication" in error_message:
        return "API key invalid hai. Apni API key check karo."

    elif "403" in error_message:
        return "API access denied hai. Account permissions check karo."

    elif "429" in error_message or "rate limit" in error_message:
        return "Rate limit exceed ho gayi. Thodi der baad try karo."

    elif "timeout" in error_message:
        return "API response mein timeout hua. Dobara try karo."

    elif "connection" in error_message:
        return "Internet connection check karo."

    else:
        return "Kuch technical problem aayi. Please dobara try karo."
