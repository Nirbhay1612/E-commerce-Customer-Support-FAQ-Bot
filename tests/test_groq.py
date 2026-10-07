from src.llm import get_groq_llm
from langchain_core.messages import SystemMessage, HumanMessage

# System prompt load karo
with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# LLM lo (ab default openai/gpt-oss-120b use hoga)
llm = get_groq_llm()

# Messages
messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content="Mera order kab tak aayega? Order number ORD-12345")
]

# Response
response = llm.invoke(messages)
print(response.content)