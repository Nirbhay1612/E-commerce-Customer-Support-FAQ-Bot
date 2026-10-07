"""
Vector Store Management.

Responsibilities:
- Load FAQ documents
- Split documents into chunks
- Create embeddings
- Create and persist Chroma vector store
- Load an existing Chroma vector store
"""

from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from src.data.load_faq import load_faq_as_documents
from src.utils.logger import (
    log_error,
    log_info,
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_PERSIST_DIRECTORY = (
    PROJECT_ROOT / "chroma_db"
)


# ============================================================
# EMBEDDING CONFIGURATION
# ============================================================

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# CHUNKING CONFIGURATION
# ============================================================

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


# ============================================================
# EMBEDDING MODEL
# ============================================================

@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Create and cache the HuggingFace embedding model.

    Returns:
        Configured HuggingFaceEmbeddings instance.

    Raises:
        RuntimeError:
            If the embedding model cannot be initialized.
    """

    try:
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME
        )

    except Exception as error:
        log_error(
            "Failed to initialize embedding model.",
            error,
        )

        raise RuntimeError(
            "Failed to initialize the embedding model."
        ) from error


# ============================================================
# TEXT SPLITTER
# ============================================================

@lru_cache(maxsize=1)
def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Create and cache the text splitter used for FAQ documents.

    Returns:
        Configured RecursiveCharacterTextSplitter.

    Raises:
        ValueError:
            If chunk configuration is invalid.
    """

    if CHUNK_SIZE <= 0:
        raise ValueError(
            "CHUNK_SIZE must be greater than 0."
        )

    if CHUNK_OVERLAP < 0:
        raise ValueError(
            "CHUNK_OVERLAP cannot be negative."
        )

    if CHUNK_OVERLAP >= CHUNK_SIZE:
        raise ValueError(
            "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
        )

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )


# ============================================================
# PATH VALIDATION
# ============================================================

def validate_persist_directory(
    persist_directory: str | Path,
) -> Path:
    """
    Validate and normalize the Chroma persistence path.

    Args:
        persist_directory:
            Chroma persistence directory.

    Returns:
        Resolved Path object.

    Raises:
        ValueError:
            If the path is invalid.
    """

    if not isinstance(
        persist_directory,
        (str, Path),
    ):
        raise ValueError(
            "persist_directory must be a string or Path."
        )

    persist_path = Path(
        persist_directory
    ).expanduser().resolve()

    return persist_path


# ============================================================
# CREATE VECTOR STORE
# ============================================================

def create_vectorstore(
    persist_directory: str | Path = DEFAULT_PERSIST_DIRECTORY,
) -> Chroma:
    """
    Create and persist the FAQ vector store.

    Pipeline:

        FAQ JSON
            ↓
        LangChain Documents
            ↓
        Text Splitting
            ↓
        Embeddings
            ↓
        Chroma Vector Store

    Args:
        persist_directory:
            Directory where Chroma stores its database.

    Returns:
        Created Chroma vector store.

    Raises:
        ValueError:
            If FAQ documents or chunks are unavailable.

        RuntimeError:
            If vector store creation fails.
    """

    persist_path = validate_persist_directory(
        persist_directory
    )

    # --------------------------------------------------------
    # Load FAQ documents
    # --------------------------------------------------------

    try:
        documents = load_faq_as_documents()

    except Exception as error:
        log_error(
            "Failed to load FAQ documents.",
            error,
        )

        raise RuntimeError(
            "Failed to load FAQ documents."
        ) from error

    if not documents:
        raise ValueError(
            "No FAQ documents were found."
        )

    # --------------------------------------------------------
    # Split documents
    # --------------------------------------------------------

    try:
        text_splitter = get_text_splitter()

        splits = text_splitter.split_documents(
            documents
        )

    except Exception as error:
        log_error(
            "Failed to split FAQ documents.",
            error,
        )

        raise RuntimeError(
            "Failed to split FAQ documents."
        ) from error

    if not splits:
        raise ValueError(
            "Document splitting produced no chunks."
        )

    # --------------------------------------------------------
    # Create persist directory
    # --------------------------------------------------------

    try:
        persist_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    except OSError as error:
        log_error(
            "Failed to create vector store directory.",
            error,
        )

        raise RuntimeError(
            "Failed to create the vector store directory."
        ) from error

    # --------------------------------------------------------
    # Create embeddings
    # --------------------------------------------------------

    embeddings = get_embedding_model()

    # --------------------------------------------------------
    # Create Chroma vector store
    # --------------------------------------------------------

    try:
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=str(
                persist_path
            ),
        )

    except Exception as error:
        log_error(
            "Failed to create Chroma vector store.",
            error,
        )

        raise RuntimeError(
            "Failed to create the FAQ vector store."
        ) from error

    # --------------------------------------------------------
    # Log creation summary
    # --------------------------------------------------------

    log_info(
        "FAQ vector store created successfully."
    )

    log_info(
        f"FAQ documents: {len(documents)}"
    )

    log_info(
        f"FAQ chunks: {len(splits)}"
    )

    log_info(
        f"Embedding model: {EMBEDDING_MODEL_NAME}"
    )

    log_info(
        f"Vector store location: {persist_path}"
    )

    return vectorstore


# ============================================================
# LOAD EXISTING VECTOR STORE
# ============================================================

@lru_cache(maxsize=4)
def load_vectorstore(
    persist_directory: str | Path = DEFAULT_PERSIST_DIRECTORY,
) -> Chroma:
    """
    Load an existing Chroma vector store.

    Args:
        persist_directory:
            Directory containing the Chroma database.

    Returns:
        Loaded Chroma vector store.

    Raises:
        FileNotFoundError:
            If the vector store does not exist.

        ValueError:
            If the path is not a directory.

        RuntimeError:
            If the vector store cannot be loaded.
    """

    persist_path = validate_persist_directory(
        persist_directory
    )

    # --------------------------------------------------------
    # Validate directory
    # --------------------------------------------------------

    if not persist_path.exists():
        raise FileNotFoundError(
            f"Vector store not found at: {persist_path}. "
            "Run 'python create_kb.py' first."
        )

    if not persist_path.is_dir():
        raise ValueError(
            f"Vector store path is not a directory: "
            f"{persist_path}"
        )

    # --------------------------------------------------------
    # Load embedding model
    # --------------------------------------------------------

    embeddings = get_embedding_model()

    # --------------------------------------------------------
    # Load Chroma
    # --------------------------------------------------------

    try:
        vectorstore = Chroma(
            persist_directory=str(
                persist_path
            ),
            embedding_function=embeddings,
        )

    except Exception as error:
        log_error(
            "Failed to load Chroma vector store.",
            error,
        )

        raise RuntimeError(
            "Failed to load the FAQ vector store."
        ) from error

    log_info(
        f"FAQ vector store loaded from: "
        f"{persist_path}"
    )

    return vectorstore