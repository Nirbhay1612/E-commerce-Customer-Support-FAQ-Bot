"""
ShopEase E-commerce Customer Support Chatbot

Responsibilities:
- Validate user input
- Manage conversation history
- Communicate with the RAG pipeline
- Clean and validate chatbot responses
- Handle API and runtime failures
- Provide safe fallback responses
- Provide terminal chat mode
"""

from typing import Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from src.chatbot.response_handler import handle_response
from src.rag.rag_chain import get_rag_response
from src.utils.error_handler import handle_error
from src.utils.fallback import detect_fallback_intent, get_fallback
from src.utils.logger import log_error, log_info


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

MAX_HISTORY_MESSAGES = 10


# -------------------------------------------------------------------
# Input Validation
# -------------------------------------------------------------------

def validate_user_message(
    user_message: Optional[str],
) -> str:
    """
    Validate and clean user input.

    Args:
        user_message: User's message.

    Returns:
        Cleaned user message.

    Raises:
        ValueError:
            If the input is invalid or empty.
    """

    if not isinstance(user_message, str):
        raise ValueError("User message must be a string.")

    cleaned_message = user_message.strip()

    if not cleaned_message:
        raise ValueError("User message cannot be empty.")

    return cleaned_message


# -------------------------------------------------------------------
# Chat History
# -------------------------------------------------------------------

def normalize_chat_history(
    chat_history: Optional[list[BaseMessage]],
) -> list[BaseMessage]:
    """
    Validate and limit conversation history.

    Only LangChain BaseMessage objects are retained.
    """

    if not chat_history:
        return []

    if not isinstance(chat_history, list):
        raise ValueError("Chat history must be a list.")

    valid_messages = [
        message
        for message in chat_history
        if isinstance(message, BaseMessage)
    ]

    return valid_messages[-MAX_HISTORY_MESSAGES:]


# -------------------------------------------------------------------
# Main Chatbot Function
# -------------------------------------------------------------------

def get_bot_response(
    user_message: str,
    chat_history: Optional[list[BaseMessage]] = None,
) -> str:
    """
    Generate a chatbot response using the RAG pipeline.

    Args:
        user_message:
            Current customer question.

        chat_history:
            Previous conversation messages.

    Returns:
        Safe, user-facing chatbot response.
    """

    # Keep the cleaned message outside the try block so it is
    # always available for fallback detection.
    cleaned_message = (
        user_message.strip()
        if isinstance(user_message, str)
        else ""
    )

    try:
        # ------------------------------------------------------------
        # Validate input
        # ------------------------------------------------------------

        cleaned_message = validate_user_message(
            user_message
        )

        # ------------------------------------------------------------
        # Normalize conversation history
        # ------------------------------------------------------------

        history = normalize_chat_history(
            chat_history
        )

        # ------------------------------------------------------------
        # Handle simple fallback intents
        # ------------------------------------------------------------

        fallback_intent = detect_fallback_intent(
            cleaned_message
        )

        if fallback_intent != "default":
            response = get_fallback(
                fallback_intent
            )

            log_info(
                f"Fallback response used: {fallback_intent}"
            )

            return response

        # ------------------------------------------------------------
        # Generate RAG response
        # ------------------------------------------------------------

        log_info(
            "Processing customer support request."
        )

        raw_response = get_rag_response(
            question=cleaned_message,
            chat_history=history,
        )

        # ------------------------------------------------------------
        # Clean and validate response
        # ------------------------------------------------------------

        response = handle_response(
            raw_response
        )

        log_info(
            "Customer support response generated successfully."
        )

        return response

    # ---------------------------------------------------------------
    # Validation errors
    # ---------------------------------------------------------------

    except ValueError as error:

        log_error(
            "Invalid chatbot request.",
            error,
        )

        # Only use intent-based fallback when we actually
        # have a valid customer message.
        if cleaned_message:
            intent = detect_fallback_intent(
                cleaned_message
            )

            return get_fallback(intent)

        return get_fallback("default")

    # ---------------------------------------------------------------
    # Unexpected / runtime / API errors
    # ---------------------------------------------------------------

    except Exception as error:

        log_error(
            "Chatbot request failed.",
            error,
        )

        return handle_error(error)


# -------------------------------------------------------------------
# Terminal Chat Mode
# -------------------------------------------------------------------

def run_chat() -> None:
    """
    Run the chatbot in terminal mode.
    """

    print("=" * 55)
    print("🛍️  E-commerce Customer Support Chatbot")
    print("🤖 Aria Support Assistant")
    print("=" * 55)

    print(
        "Type 'exit', 'quit', or 'bye' to end the chat."
    )

    print("=" * 55)

    chat_history: list[BaseMessage] = []

    while True:

        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                print(
                    "Aria: Please enter a question."
                )
                continue

            if user_input.lower() in {
                "exit",
                "quit",
                "bye",
            }:
                print(
                    "\nAria: Thank you for chatting "
                    "with us. Have a great day! 😊"
                )
                break

            response = get_bot_response(
                user_message=user_input,
                chat_history=chat_history,
            )

            print(
                f"\nAria: {response}"
            )

            # --------------------------------------------------------
            # Store conversation
            # --------------------------------------------------------

            chat_history.extend(
                [
                    HumanMessage(
                        content=user_input
                    ),
                    AIMessage(
                        content=response
                    ),
                ]
            )

            # --------------------------------------------------------
            # Limit history
            # --------------------------------------------------------

            chat_history = chat_history[
                -MAX_HISTORY_MESSAGES:
            ]

        except KeyboardInterrupt:

            print(
                "\n\nAria: Chat ended. Goodbye! 👋"
            )
            break

        except EOFError:

            print(
                "\n\nAria: Chat ended. Goodbye! 👋"
            )
            break

        except Exception as error:

            log_error(
                "Terminal chat failed.",
                error,
            )

            print(
                "\nAria: Sorry, something went wrong."
            )


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    run_chat()