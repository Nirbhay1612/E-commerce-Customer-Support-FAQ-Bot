from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.load_faq import load_faq_as_documents

def create_vectorstore(persist_directory: str = "chroma_db"):
    # 1. Load FAQs
    documents = load_faq_as_documents()

    # 2. Split documents (optional but recommended)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    splits = text_splitter.split_documents(documents)

    # 3. Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Create & save vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    print(f"✅ Vector store created at: {persist_directory}")
    return vectorstore


def load_vectorstore(persist_directory: str = "chroma_db"):
    """Already created vector store ko load karne ke liye"""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    return vectorstore