"""
FAQ Data Loader

Responsible for:
- Loading FAQ data from JSON
- Validating FAQ structure
- Cleaning FAQ content
- Converting FAQs into LangChain Documents
"""

import json
from pathlib import Path
from typing import Any

from langchain_core.documents import Document


# -------------------------------------------------------------------
# Project paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_FAQ_PATH = PROJECT_ROOT / "data" / "faq.json"


# -------------------------------------------------------------------
# Validation helpers
# -------------------------------------------------------------------

REQUIRED_FIELDS = {"question", "answer"}


def _validate_faq_entry(
    item: Any,
    index: int,
    seen_questions: set[str],
) -> dict[str, Any]:
    """
    Validate and clean a single FAQ entry.

    Args:
        item: Raw FAQ entry.
        index: FAQ index.
        seen_questions: Set of normalized questions used to
            detect duplicates.

    Returns:
        Cleaned FAQ dictionary.

    Raises:
        ValueError:
            If the FAQ entry is invalid.
    """

    entry_number = index + 1

    if not isinstance(item, dict):
        raise ValueError(
            f"FAQ entry #{entry_number} must be a JSON object."
        )

    # Check required fields
    missing_fields = REQUIRED_FIELDS - item.keys()

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))

        raise ValueError(
            f"FAQ entry #{entry_number} is missing required "
            f"field(s): {missing}"
        )

    # Validate question
    question = item["question"]

    if not isinstance(question, str):
        raise ValueError(
            f"FAQ entry #{entry_number}: "
            "'question' must be a string."
        )

    question = question.strip()

    if not question:
        raise ValueError(
            f"FAQ entry #{entry_number}: "
            "'question' cannot be empty."
        )

    # Validate answer
    answer = item["answer"]

    if not isinstance(answer, str):
        raise ValueError(
            f"FAQ entry #{entry_number}: "
            "'answer' must be a string."
        )

    answer = answer.strip()

    if not answer:
        raise ValueError(
            f"FAQ entry #{entry_number}: "
            "'answer' cannot be empty."
        )

    # Detect duplicate questions
    normalized_question = " ".join(question.lower().split())

    if normalized_question in seen_questions:
        raise ValueError(
            f"Duplicate FAQ question found at entry "
            f"#{entry_number}: '{question}'"
        )

    seen_questions.add(normalized_question)

    # Optional ID
    faq_id = item.get("id")

    if faq_id is not None:
        faq_id = str(faq_id).strip()

        if not faq_id:
            faq_id = None

    # Optional category
    category = item.get("category")

    if category is not None:
        if not isinstance(category, str):
            raise ValueError(
                f"FAQ entry #{entry_number}: "
                "'category' must be a string."
            )

        category = category.strip()

        if not category:
            category = None

    return {
        "id": faq_id,
        "question": question,
        "answer": answer,
        "category": category,
    }


# -------------------------------------------------------------------
# FAQ loading
# -------------------------------------------------------------------

def load_faq_data(
    file_path: str | Path = DEFAULT_FAQ_PATH,
) -> list[dict[str, Any]]:
    """
    Load, validate, and clean FAQ data from a JSON file.

    Args:
        file_path: Path to the FAQ JSON file.

    Returns:
        A list of validated FAQ dictionaries.

    Raises:
        FileNotFoundError:
            If the FAQ file does not exist.

        ValueError:
            If the JSON structure or FAQ data is invalid.
    """

    path = Path(file_path)

    # Check whether file exists
    if not path.exists():
        raise FileNotFoundError(
            f"FAQ file not found: {path}"
        )

    # Check whether path is a file
    if not path.is_file():
        raise ValueError(
            f"FAQ path is not a valid file: {path}"
        )

    # Load JSON
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON format in FAQ file: {path}. "
            f"Line {error.lineno}, column {error.colno}."
        ) from error

    except OSError as error:
        raise RuntimeError(
            f"Unable to read FAQ file: {path}"
        ) from error

    # Validate top-level structure
    if not isinstance(data, list):
        raise ValueError(
            "FAQ JSON must contain a list of FAQ objects."
        )

    if not data:
        raise ValueError(
            "FAQ file is empty. Add at least one FAQ."
        )

    # Validate and clean FAQ entries
    validated_faqs: list[dict[str, Any]] = []
    seen_questions: set[str] = set()

    for index, item in enumerate(data):
        validated_item = _validate_faq_entry(
            item=item,
            index=index,
            seen_questions=seen_questions,
        )

        # Generate stable fallback ID if none exists
        if not validated_item["id"]:
            validated_item["id"] = f"faq_{index + 1:03d}"

        validated_faqs.append(validated_item)

    return validated_faqs


# -------------------------------------------------------------------
# LangChain document conversion
# -------------------------------------------------------------------

def load_faq_as_documents(
    file_path: str | Path = DEFAULT_FAQ_PATH,
) -> list[Document]:
    """
    Load FAQ data and convert it into LangChain Documents.

    Args:
        file_path: Path to the FAQ JSON file.

    Returns:
        A list of LangChain Document objects.
    """

    faq_data = load_faq_data(file_path)

    documents: list[Document] = []

    for item in faq_data:
        question = item["question"]
        answer = item["answer"]

        content = (
            f"Question: {question}\n"
            f"Answer: {answer}"
        )

        metadata = {
            "faq_id": item["id"],
            "question": question,
        }

        # Only add category when available
        if item.get("category"):
            metadata["category"] = item["category"]

        document = Document(
            page_content=content,
            metadata=metadata,
        )

        documents.append(document)

    return documents