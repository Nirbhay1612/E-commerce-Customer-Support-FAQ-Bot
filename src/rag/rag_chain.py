"""
Retrieval-Augmented Generation (RAG) Chain.

Responsibilities:
- Retrieve relevant FAQ documents
- Format retrieved documents into context
- Build the support prompt
- Include relevant conversation history
- Send context and question to the LLM
- Return the final response
"""

from functools import lru_cache
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm import get_groq_llm
from src.rag.retriever import retrieve_faq


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_TOP_K = 3
MAX_HISTORY_MESSAGES = 6

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAG_PROMPT_PATH = (
    PROJECT_ROOT / "prompts" / "rag_prompt.txt"
)


# ============================================================
# PROMPT LOADER
# ============================================================

def load_rag_prompt(
    path: Path = RAG_PROMPT_PATH,
) -> str:
    """
    Load the RAG prompt from the prompts directory.

    Args:
        path:
            Path to the RAG prompt file.

    Returns:
        Prompt template as a string.

    Raises:
        FileNotFoundError:
            If the prompt file does not exist.

        ValueError:
            If the prompt file is empty.

        OSError:
            If the prompt cannot be read.
    """

    try:
        prompt = path.read_text(
            encoding="utf-8"
        ).strip()

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"RAG prompt file not found: {path}"
        ) from error

    except OSError as error:
        raise OSError(
            f"Unable to read RAG prompt: {path}"
        ) from error

    if not prompt:
        raise ValueError(
            "RAG prompt cannot be empty."
        )

    return prompt


# ============================================================
# DOCUMENT FORMATTING
# ============================================================

def format_docs(
    documents: list[Document],
) -> str:
    """
    Convert retrieved FAQ documents into LLM context.

    Args:
        documents:
            Retrieved FAQ documents.

    Returns:
        Formatted FAQ context.
    """

    if not documents:
        return (
            "No relevant FAQ information was found."
        )

    formatted_documents: list[str] = []

    for index, document in enumerate(
        documents,
        start=1,
    ):
        if not isinstance(
            document,
            Document,
        ):
            continue

        content = (
            document.page_content or ""
        ).strip()

        if not content:
            continue

        metadata = document.metadata or {}

        category = str(
            metadata.get("category", "")
        ).strip()

        if category:
            formatted_documents.append(
                f"FAQ {index} "
                f"(Category: {category}):\n"
                f"{content}"
            )
        else:
            formatted_documents.append(
                f"FAQ {index}:\n"
                f"{content}"
            )

    if not formatted_documents:
        return (
            "No relevant FAQ information was found."
        )

    return "\n\n".join(
        formatted_documents
    )


# ============================================================
# CHAT HISTORY FORMATTING
# ============================================================

def format_chat_history(
    chat_history: list | None,
) -> str:
    """
    Convert previous conversation messages into
    a compact text representation.

    Only the most recent messages are included.

    Args:
        chat_history:
            Previous conversation messages.

    Returns:
        Formatted conversation history.
    """

    if not chat_history:
        return "No previous conversation."

    history_lines: list[str] = []

    recent_messages = chat_history[
        -MAX_HISTORY_MESSAGES:
    ]

    for message in recent_messages:

        if isinstance(message, dict):
            role = message.get(
                "role",
                "",
            )
            content = message.get(
                "content",
                "",
            )

        else:
            role = getattr(
                message,
                "type",
                "",
            )
            content = getattr(
                message,
                "content",
                "",
            )

        role = str(role).strip()
        content = str(content).strip()

        if not content:
            continue

        if role in {"human", "user"}:
            role = "Customer"

        elif role in {"ai", "assistant"}:
            role = "Assistant"

        else:
            role = "Message"

        history_lines.append(
            f"{role}: {content}"
        )

    if not history_lines:
        return "No previous conversation."

    return "\n".join(history_lines)


# ============================================================
# RAG CHAIN
# ============================================================

@lru_cache(maxsize=1)
def create_rag_chain():
    """
    Create and cache the complete RAG pipeline.

    Flow:

        User Question
              ↓
        FAQ Retriever
              ↓
        Relevant Documents
              ↓
        Context Formatting
              ↓
        RAG Prompt
              ↓
        Groq LLM
              ↓
        Final Answer

    Returns:
        Configured LangChain RAG chain.
    """

    # --------------------------------------------------------
    # Initialize LLM
    # --------------------------------------------------------

    llm = get_groq_llm()

    # --------------------------------------------------------
    # Load prompt
    # --------------------------------------------------------

    rag_prompt = load_rag_prompt()

    prompt = ChatPromptTemplate.from_template(
        rag_prompt
    )

    # --------------------------------------------------------
    # Build RAG chain
    # --------------------------------------------------------

    def build_context(
        inputs: dict,
    ) -> str:
        """
        Retrieve and format FAQ context
        for the current question.
        """

        question = inputs["question"]

        documents = retrieve_faq(
            query=question,
            k=DEFAULT_TOP_K,
        )

        return format_docs(
            documents
        )

    rag_chain = (
        {
            "context": build_context,
            "question": lambda inputs: inputs[
                "question"
            ],
            "chat_history": lambda inputs: inputs[
                "chat_history"
            ],
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# ============================================================
# PUBLIC RESPONSE FUNCTION
# ============================================================

def get_rag_response(
    question: str,
    chat_history: list | None = None,
) -> str:
    """
    Generate a customer-support response using
    the RAG pipeline.

    Args:
        question:
            Customer's current question.

        chat_history:
            Previous conversation messages.

    Returns:
        Generated support response.

    Raises:
        ValueError:
            If the question or chat history is invalid.
    """

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    if not isinstance(
        question,
        str,
    ):
        raise ValueError(
            "Question must be a string."
        )

    question = question.strip()

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

    # --------------------------------------------------------
    # Validate chat history
    # --------------------------------------------------------

    if chat_history is None:
        chat_history = []

    if not isinstance(
        chat_history,
        list,
    ):
        raise ValueError(
            "Chat history must be a list."
        )

    # --------------------------------------------------------
    # Format history
    # --------------------------------------------------------

    formatted_history = format_chat_history(
        chat_history
    )

    # --------------------------------------------------------
    # Run RAG pipeline
    # --------------------------------------------------------

    chain = create_rag_chain()

    response = chain.invoke(
        {
            "question": question,
            "chat_history": formatted_history,
        }
    )

    # --------------------------------------------------------
    # Validate response
    # --------------------------------------------------------

    if response is None:
        raise ValueError(
            "RAG chain returned an empty response."
        )

    response = str(response).strip()

    if not response:
        raise ValueError(
            "RAG chain returned an empty response."
        )

    return response