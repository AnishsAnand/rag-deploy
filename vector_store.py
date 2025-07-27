from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, CSVLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import os

def load_text_documents(folder="data/scraped_docs"):
    docs = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        try:
            if file.endswith(".txt"):
                docs.extend(TextLoader(path).load())
            elif file.endswith(".csv"):
                docs.extend(CSVLoader(path).load())
            elif file.endswith(".pdf"):
                docs.extend(PyPDFLoader(path).load())
        except Exception as e:
            print(f"Loading failed for {file}: {e}")
    return docs

def store_in_vector_db():
    docs = load_text_documents()
    if not docs:
        print("No documents to vectorize.")
        return
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory="chroma_combined_knowledge")

    print(f"Stored {len(chunks)} chunks in ChromaDB.")
    return db
