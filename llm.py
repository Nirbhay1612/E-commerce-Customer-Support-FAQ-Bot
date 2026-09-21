import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_groq_llm(
    model: str = "openai/gpt-oss-120b",
    temperature: float = 0.3
):
    """
    Returns a ChatGroq LLM instance using openai/gpt-oss-120b by default.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        raise ValueError(
            "GROQ_API_KEY not set properly.\n"
            "1. Get free API key from: https://console.groq.com/keys\n"
            "2. Put it in .env file: GROQ_API_KEY=your_actual_key"
        )
    
    return ChatGroq(
        model=model,
        temperature=temperature,
        groq_api_key=api_key,
    )