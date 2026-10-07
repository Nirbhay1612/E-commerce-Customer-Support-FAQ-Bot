"""
ShopEase Streamlit Application

Responsibilities:
- Provide the customer-facing Streamlit UI
- Manage Streamlit session state
- Display conversation history
- Collect user questions
- Send previous conversation history to the chatbot
- Display chatbot responses
"""

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from src.chatbot.chatbot import get_bot_response


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ShopEase Support",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONSTANTS
# ============================================================

APP_NAME = "ShopEase Support"

SUGGESTED_QUESTIONS = [
    "Where is my order?",
    "What is your return policy?",
    "How long does delivery take?",
    "How do refunds work?",
]


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .welcome-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 20px;
    }

    .footer {
        text-align: center;
        color: #888;
        font-size: 12px;
        margin-top: 30px;
        padding-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def build_chat_history(
    messages: list[dict],
) -> list:
    """
    Convert Streamlit messages into LangChain messages.

    Args:
        messages:
            Streamlit chat messages.

    Returns:
        List of LangChain HumanMessage and AIMessage objects.
    """

    chat_history = []

    for message in messages:

        role = message.get("role")
        content = message.get("content", "").strip()

        if not content:
            continue

        if role == "user":
            chat_history.append(
                HumanMessage(content=content)
            )

        elif role == "assistant":
            chat_history.append(
                AIMessage(content=content)
            )

    return chat_history


def clear_chat() -> None:
    """Clear the current conversation."""

    st.session_state.messages = []


def generate_response(
    user_input: str,
    previous_messages: list[dict],
) -> str:
    """
    Generate a chatbot response.

    Only previous messages are passed to the chatbot.
    The current user message is handled separately.
    """

    chat_history = build_chat_history(
        previous_messages
    )

    return get_bot_response(
        user_message=user_input,
        chat_history=chat_history,
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛍️ ShopEase Support</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "AI-powered customer support assistant"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛍️ ShopEase")

    st.caption("Customer Support")

    st.divider()

    if st.button(
        "🆕 New Chat",
        use_container_width=True,
    ):
        clear_chat()
        st.rerun()

    st.divider()

    st.subheader("About")

    st.write(
        "Ask questions about orders, shipping, returns, "
        "refunds, payments, products and store policies."
    )

    st.divider()

    st.subheader("Features")

    st.markdown(
        """
        - 🤖 AI-powered responses
        - 📚 FAQ knowledge base
        - 🔎 RAG-powered retrieval
        - 💬 Conversation history
        - 🛡️ Error handling
        """
    )

    st.divider()

    st.caption(
        f"{APP_NAME} • AI Assistant"
    )


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-box">

        ### 👋 Welcome to ShopEase Support

        I'm here to help you with:

        - 📦 Orders
        - 🚚 Shipping & delivery
        - 🔄 Returns & exchanges
        - 💰 Refunds
        - 💳 Payments
        - 🛍️ Product information

        Ask me anything about your ShopEase order or policies.

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

selected_question = None

if not st.session_state.messages:

    st.subheader("💡 Suggested questions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            f"📦 {SUGGESTED_QUESTIONS[0]}",
            use_container_width=True,
        ):
            selected_question = SUGGESTED_QUESTIONS[0]

        if st.button(
            f"🔄 {SUGGESTED_QUESTIONS[1]}",
            use_container_width=True,
        ):
            selected_question = SUGGESTED_QUESTIONS[1]

    with col2:

        if st.button(
            f"🚚 {SUGGESTED_QUESTIONS[2]}",
            use_container_width=True,
        ):
            selected_question = SUGGESTED_QUESTIONS[2]

        if st.button(
            f"💰 {SUGGESTED_QUESTIONS[3]}",
            use_container_width=True,
        ):
            selected_question = SUGGESTED_QUESTIONS[3]


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ============================================================
# USER INPUT
# ============================================================

user_input = st.chat_input(
    "Ask about orders, returns, shipping..."
)

if selected_question:
    user_input = selected_question


# ============================================================
# HANDLE USER MESSAGE
# ============================================================

if user_input:

    user_input = user_input.strip()

    if not user_input:
        st.warning("Please enter a question.")
        st.stop()

    # --------------------------------------------------------
    # Preserve previous history BEFORE adding current message
    # --------------------------------------------------------

    previous_messages = list(
        st.session_state.messages
    )

    # --------------------------------------------------------
    # Add current user message to UI history
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = generate_response(
                user_input=user_input,
                previous_messages=previous_messages,
            )

        st.markdown(response)

    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
    ShopEase Support • AI Customer Support Assistant
    </div>
    """,
    unsafe_allow_html=True,
)