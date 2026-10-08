# 🛍️ ShopEase E-commerce Customer Support Chatbot

An AI-powered **E-commerce Customer Support FAQ Chatbot** built with Python, Streamlit, LangChain, ChromaDB, Hugging Face embeddings, and Groq.

The chatbot uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant information from an e-commerce FAQ knowledge base and generate concise, context-aware customer support responses.

---
## 🌐 Live Demo

Try the deployed chatbot here:

👉 **[ShopEase Customer Support Chatbot](https://e-commerce-customer-support-faq-bot-4pnnkedbbfgxan7r8sglcs.streamlit.app/)**

> The application is deployed using Streamlit.

## 📌 Overview

ShopEase Customer Support Chatbot is designed to automate common e-commerce customer support queries.

The system can answer questions related to topics such as:

- Orders
- Shipping and delivery
- Returns
- Refunds
- Payments
- Other FAQ-based customer support queries

Instead of relying only on the LLM's general knowledge, the chatbot retrieves relevant information from a structured FAQ knowledge base before generating a response.

This helps reduce hallucinations and keeps responses grounded in the available business information.

---
## 🛠️ Tech Stack 
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-API-F55036?style=for-the-badge)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=for-the-badge&logo=databricks&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Sentence Transformers](https://img.shields.io/badge/Sentence%20Transformers-4B8BBE?style=for-the-badge)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)


## ✨ Features

- 🤖 AI-powered customer support chatbot
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔎 Semantic FAQ retrieval
- 🗄️ ChromaDB vector database
- 🔤 Hugging Face sentence-transformer embeddings
- ⚡ Groq LLM integration
- 💬 Conversation history support
- 🛡️ Safe fallback responses
- 🚨 Centralized error handling
- 🧹 Response cleaning and validation
- 📝 Centralized application logging
- 🎯 Suggested customer questions
- 🖥️ Streamlit web interface
- 🧪 Automated test suite
- ✅ 125 automated tests passing

---


## 📂 Project Structure
E-commerce Customer Support FAQ Chatbot/
│
├── app.py
├── create_kb.py
├── listmodels.py
├── requirements.txt
├── pytest.ini
├── README.md
├── .gitignore
├── .env.example
│
├── Data/
│   ├── faq.json
│   └── products.json
│
├── prompts/
│   ├── fallback_prompt.txt
│   ├── rag_prompt.txt
│   └── system_prompt.txt
│
├── src/
│   ├── __init__.py
│   │
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   └── response_handler.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   └── load_faq.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── llm.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── rag_chain.py
│   │   ├── retriever.py
│   │   └── vectorstore.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── error_handler.py
│       ├── fallback.py
│       └── logger.py
│
└── tests/
    ├── __init__.py
    ├── test_api_failure.py
    ├── test_chatbot.py
    ├── test_error_handler.py
    ├── test_fallback.py
    ├── test_faq.py
    ├── test_groq.py
    ├── test_rag.py
    ├── test_retriever.py
    └── test_response_handler.py



##🔄 RAG Workflow
The chatbot follows this process:
User Question
      ↓
Input Validation
      ↓
FAQ Retrieval
      ↓
Semantic Similarity Search
      ↓
Relevant FAQ Context
      ↓
RAG Prompt
      ↓
Groq LLM
      ↓
Response Cleaning
      ↓
Response Validation
      ↓
Final Answer

## 🚀 Future Improvements
Potential future improvements include:
- Real-time order tracking integration
- Customer account integration
- Product search and recommendation
- Multilingual support
- Human-agent handoff
- Customer support analytics
- Authentication
- Conversation analytics
- Production monitoring
- Additional business knowledge sources 

## 🎯 Project Objective
The goal of this project was to build a practical, production-oriented e-commerce customer support chatbot while demonstrating skills in:
- Python development
- LLM integration
- RAG architecture
- Vector databases
- Semantic search
- Prompt engineering
- API integration
- Error handling
- Testing
- Streamlit application development
- Git and GitHub workflow




## 🧑 Author
Nirbhay Tembhurne
