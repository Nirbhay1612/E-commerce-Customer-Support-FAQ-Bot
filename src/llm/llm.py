"""
LLM Configuration

Responsible for:
- Loading environment variables
- Validating the Groq API key
- Configuring the Groq chat model
- Creating the reusable LLM instance
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import SecretStr


# -------------------------------------------------------------------
# Environment
# -------------------------------------------------------------------

load_dotenv()


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)

LLM_TEMPERATURE = float(
    os.getenv("LLM_TEMPERATURE", "0.2")
)

LLM_TIMEOUT = int(
    os.getenv("LLM_TIMEOUT", "30")
)

LLM_MAX_RETRIES = int(
    os.getenv("LLM_MAX_RETRIES", "2")
)


# -------------------------------------------------------------------
# API Key
# -------------------------------------------------------------------

def get_groq_api_key() -> str:
    """
    Retrieve and validate the Groq API key.

    Returns:
        Valid Groq API key.

    Raises:
        ValueError:
            If GROQ_API_KEY is missing or empty.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or not api_key.strip():
        raise ValueError(
            "GROQ_API_KEY is not configured. "
            "Add your API key to the .env file."
        )

    return api_key.strip()


# -------------------------------------------------------------------
# LLM Factory
# -------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_groq_llm() -> ChatGroq:
    """
    Create and return the configured Groq LLM.

    The LLM instance is cached so that the application does not
    unnecessarily recreate the model configuration on every request.

    Returns:
        Configured ChatGroq instance.

    Raises:
        ValueError:
            If GROQ_API_KEY is missing.
    """

    api_key = get_groq_api_key()

    return ChatGroq(
        model=GROQ_MODEL,
        temperature=LLM_TEMPERATURE,
        api_key=SecretStr(api_key),
        timeout=LLM_TIMEOUT,
        max_retries=LLM_MAX_RETRIES,
    )