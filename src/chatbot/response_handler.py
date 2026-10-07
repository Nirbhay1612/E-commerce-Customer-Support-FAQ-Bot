"""
Response Handler

Responsible for:
- Cleaning LLM responses
- Validating generated responses
- Normalizing response formatting
- Enforcing a safe response length
- Providing a consistent final response
"""

from typing import Any


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

MAX_RESPONSE_LENGTH = 4000


# -------------------------------------------------------------------
# Response Cleaning
# -------------------------------------------------------------------

def clean_response(response: Any) -> str:
    """
    Clean and normalize a response returned by the LLM or RAG pipeline.

    Args:
        response: Raw response returned by the LLM or RAG chain.

    Returns:
        A cleaned response string.
    """

    if response is None:
        return ""

    # Plain string response
    if isinstance(response, str):
        content = response

    # LangChain AIMessage or similar response object
    elif hasattr(response, "content"):
        content = response.content

    # Fallback for other response types
    else:
        content = str(response)

    if content is None:
        return ""

    content = str(content).strip()

    if not content:
        return ""

    # Normalize line endings and trailing whitespace.
    lines = content.splitlines()

    cleaned_lines = [
        line.rstrip()
        for line in lines
    ]

    content = "\n".join(cleaned_lines).strip()

    if not content:
        return ""

    # Prevent excessively large responses.
    if len(content) > MAX_RESPONSE_LENGTH:
        content = content[:MAX_RESPONSE_LENGTH].rstrip()

        # Avoid ending in the middle of a word.
        last_space = content.rfind(" ")

        if last_space > 0:
            content = content[:last_space].rstrip()

        content += "..."

    return content


# -------------------------------------------------------------------
# Response Validation
# -------------------------------------------------------------------

def is_valid_response(response: Any) -> bool:
    """
    Check whether a response contains usable content.

    Args:
        response: Response returned by the LLM or RAG pipeline.

    Returns:
        True if the response contains usable text, otherwise False.
    """

    return bool(clean_response(response))


# -------------------------------------------------------------------
# Final Response Handler
# -------------------------------------------------------------------

def handle_response(response: Any) -> str:
    """
    Clean and validate the final chatbot response.

    Args:
        response: Raw response from the LLM or RAG pipeline.

    Returns:
        A cleaned and validated response string.

    Raises:
        ValueError:
            If the response is empty or invalid.
    """

    cleaned_response = clean_response(response)

    if not cleaned_response:
        raise ValueError(
            "The chatbot returned an empty response."
        )

    return cleaned_response