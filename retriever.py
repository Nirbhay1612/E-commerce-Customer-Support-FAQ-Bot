from src.retrieval.vectorstore import load_vectorstore

def get_retriever(k: int = 3):
    """
    FAQ Retrieval System
    k = kitne relevant FAQs return kare
    """
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    return retriever


def retrieve_faq(query: str, k: int = 3):
    """
    User ke question se relevant FAQs nikaalo
    """
    retriever = get_retriever(k=k)
    results = retriever.invoke(query)

    print(f"\n🔍 Query: {query}")
    print(f"📄 Found {len(results)} relevant FAQs:\n")

    for i, doc in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f"Category : {doc.metadata.get('category')}")
        print(f"Question : {doc.metadata.get('question')}")
        print(f"Content  : {doc.page_content[:200]}...")
        print()

    return results