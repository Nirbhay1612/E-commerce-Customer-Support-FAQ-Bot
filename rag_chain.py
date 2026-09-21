from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.llm import get_groq_llm
from src.retrieval.retriever import get_retriever

def create_rag_chain():
    llm = get_groq_llm()
    retriever = get_retriever(k=3)

    template = """You are a helpful e-commerce customer support assistant.
Use the following FAQ context to answer the user's question.
If the answer is not in the context, politely say you don't know.

Context:
{context}

Question: {question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain