"""
E-commerce Customer Support Chatbot
with System Prompt + Fallback Responses
"""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from fallback import handle_api_error
from src.llm import get_groq_llm
from src.fallback import get_fallback, detect_fallback_intent


def load_system_prompt(path: str = "prompts/system_prompt.txt") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_bot_response(user_message: str, chat_history: list | None = None) -> str:
    """
    Main function to get response from LLM with fallback support.
    """
    if chat_history is None:
        chat_history = []

    try:
        llm = get_groq_llm()
        system_prompt = load_system_prompt()

        messages = [SystemMessage(content=system_prompt)]
        
        # Add previous conversation
        for msg in chat_history:
            messages.append(msg)
        
        # Current user message
        messages.append(HumanMessage(content=user_message))

        response = llm.invoke(messages)
        content = response.content.strip() if response.content else ""

        # If LLM returns empty response → use fallback
        if not content:
            intent = detect_fallback_intent(user_message)
            return get_fallback(intent)

        return content

    except Exception as e:
        error_str = str(e).lower()

        # Decide which fallback to use based on error type
        if "timeout" in error_str or "timed out" in error_str:
            return get_fallback("timeout")
        elif "api" in error_str or "rate" in error_str or "401" in error_str or "403" in error_str:
            return get_fallback("api_error")
        else:
            # Try keyword-based fallback as last resort
            intent = detect_fallback_intent(user_message)
            return get_fallback(intent)


def run_chat():
    """Simple continuous chat loop"""
    print("=" * 50)
    print("🛍️  E-commerce Support Chatbot (Aria)")
    print("Type 'exit' or 'quit' to end the chat")
    print("=" * 50)

    chat_history = []

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nAria: Thank you for chatting with us. Have a great day! 😊")
            break

        response = get_bot_response(user_input, chat_history)
        print(f"\nAria: {response}")

        # Save to history for multi-turn conversation
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))

        # Keep history manageable (last 10 messages)
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]


if __name__ == "__main__":
    run_chat()