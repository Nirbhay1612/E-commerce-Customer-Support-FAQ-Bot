"""
ShopEase Knowledge Base Builder.

This script creates or rebuilds the FAQ vector store.

Pipeline:
    FAQ Data
        ↓
    Document Loading
        ↓
    Text Splitting
        ↓
    Embeddings
        ↓
    Chroma Vector Store

Usage:
    python create_kb.py
"""

import sys

from src.rag.vectorstore import create_vectorstore
from src.utils.logger import log_error, log_info


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_NAME = "ShopEase Knowledge Base Builder"


# ============================================================
# MAIN
# ============================================================

def main() -> int:
    """
    Create or rebuild the FAQ knowledge base.

    Returns:
        0 if the knowledge base was created successfully.
        1 if creation failed.
    """

    print("=" * 60)
    print(f"🛍️  {APP_NAME}")
    print("=" * 60)

    print("\n🔄 Building FAQ knowledge base...")

    try:
        vectorstore = create_vectorstore()

        if vectorstore is None:
            raise RuntimeError(
                "Vector store creation returned no result."
            )

        print("\n" + "=" * 60)
        print("✅ Knowledge base created successfully.")
        print("📚 FAQ embeddings are ready for retrieval.")
        print("=" * 60)

        log_info(
            "Knowledge base build completed successfully."
        )

        return 0

    except FileNotFoundError as error:
        print("\n❌ Required file not found.")
        print("   Please check your FAQ data and project paths.")

        log_error(
            "Knowledge base build failed: required file not found.",
            error,
        )

        return 1

    except ValueError as error:
        print("\n❌ Invalid knowledge-base data.")
        print(
            f"   {error}"
        )

        log_error(
            "Knowledge base build failed: invalid data.",
            error,
        )

        return 1

    except RuntimeError as error:
        print("\n❌ Knowledge base creation failed.")
        print(
            f"   {error}"
        )

        log_error(
            "Knowledge base build failed.",
            error,
        )

        return 1

    except Exception as error:
        print(
            "\n❌ Unexpected error while "
            "creating the knowledge base."
        )

        print(
            "   Please check the application logs "
            "for more details."
        )

        log_error(
            "Unexpected knowledge base build error.",
            error,
        )

        return 1


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    sys.exit(main())