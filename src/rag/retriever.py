"""
FAQ Retriever.

Responsibilities:
- Load the FAQ vector store
- Create a configured retriever
- Validate retrieval parameters
- Retrieve relevant FAQ documents
- Validate retrieved documents
"""

from functools import lru_cache

from langchain_core.documents import Document

from src.rag.vectorstore import load_vectorstore


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_TOP_K = 3
MAX_TOP_K = 10


# ============================================================
# VALIDATION
# ============================================================

def validate_top_k(k: int) -> int:
    """
    Validate the number of documents to retrieve.

    Args:
        k:
            Number of documents to retrieve.

    Returns:
        Validated k value.

    Raises:
        ValueError:
            If k is invalid.
    """

    if isinstance(k, bool) or not isinstance(k, int):
        raise ValueError(
            "k must be an integer."
        )

    if k < 1:
        raise ValueError(
            "k must be at least 1."
        )

    if k > MAX_TOP_K:
        raise ValueError(
            f"k cannot be greater than {MAX_TOP_K}."
        )

    return k


# ============================================================
# CREATE RETRIEVER
# ============================================================

@lru_cache(maxsize=MAX_TOP_K)
def get_retriever(
    k: int = DEFAULT_TOP_K,
):
    """
    Create and cache the FAQ retriever.

    Args:
        k:
            Number of relevant FAQ documents to retrieve.

    Returns:
        Configured LangChain retriever.

    Raises:
        ValueError:
            If k is invalid.

        RuntimeError:
            If the vector store or retriever cannot be created.
    """

    k = validate_top_k(k)

    # --------------------------------------------------------
    # Load vector store
    # --------------------------------------------------------

    try:
        vectorstore = load_vectorstore()

    except Exception as error:
        raise RuntimeError(
            "Failed to load the FAQ vector store."
        ) from error

    if vectorstore is None:
        raise RuntimeError(
            "FAQ vector store is unavailable."
        )

    # --------------------------------------------------------
    # Create retriever
    # --------------------------------------------------------

    try:
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k,
            },
        )

    except Exception as error:
        raise RuntimeError(
            "Failed to create the FAQ retriever."
        ) from error

    return retriever


# ============================================================
# RETRIEVE FAQ DOCUMENTS
# ============================================================

def retrieve_faq(
    query: str,
    k: int = DEFAULT_TOP_K,
) -> list[Document]:
    """
    Retrieve FAQ documents relevant to a user query.

    Args:
        query:
            User's question.

        k:
            Number of relevant documents to retrieve.

    Returns:
        List of relevant FAQ documents.

    Raises:
        ValueError:
            If query or k is invalid.

        RuntimeError:
            If retrieval fails.
    """

    # --------------------------------------------------------
    # Validate query
    # --------------------------------------------------------

    if not isinstance(query, str):
        raise ValueError(
            "Query must be a string."
        )

    query = query.strip()

    if not query:
        raise ValueError(
            "Query cannot be empty."
        )

    # --------------------------------------------------------
    # Validate top-k
    # --------------------------------------------------------

    k = validate_top_k(k)

    # --------------------------------------------------------
    # Retrieve documents
    # --------------------------------------------------------

    try:
        retriever = get_retriever(k=k)

        results = retriever.invoke(query)

    except ValueError:
        raise

    except Exception as error:
        raise RuntimeError(
            "FAQ document retrieval failed."
        ) from error

    # --------------------------------------------------------
    # Validate results
    # --------------------------------------------------------

    if not results:
        return []

    valid_documents = [
        document
        for document in results
        if isinstance(document, Document)
    ]

    return valid_documents