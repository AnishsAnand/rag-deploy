from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA

CHROMA_PATH = "chroma_combined_knowledge"

def create_qa_chain():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(embedding_function=embeddings, persist_directory=CHROMA_PATH)
    retriever = db.as_retriever()
    llm = ChatOllama(model="deepseek-v2:latest")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain
