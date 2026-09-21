import json
from pathlib import Path
from langchain_core.documents import Document

def load_faq_data(file_path: str = "data/knowledge_base/faq.json"):
    """
    Load FAQ JSON file and return list of dictionaries
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"FAQ file not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"✅ Loaded {len(data)} FAQs successfully")
    return data


def load_faq_as_documents(file_path: str = "data/knowledge_base/faq.json"):
    """
    Load FAQ and convert to LangChain Documents (for RAG)
    """
    faq_data = load_faq_data(file_path)

    documents = []
    for item in faq_data:
        content = f"Question: {item['question']}\nAnswer: {item['answer']}"
        
        doc = Document(
            page_content=content,
            metadata={
                "id": item.get("id"),
                "category": item.get("category"),
                "question": item.get("question")
            }
        )
        documents.append(doc)

    return documents