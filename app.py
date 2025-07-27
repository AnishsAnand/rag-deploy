from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from sentiment import analyze_sentiment
import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Set static folder for serving frontend
app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

CHROMA_PATH = "chroma_combined_knowledge"
DB_PATH = "feedback.db"
CONFIDENCE_THRESHOLD = 0.6

def create_qa_chain():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(embedding_function=embeddings, persist_directory=CHROMA_PATH)
    retriever = db.as_retriever()
    llm = ChatOllama(model="deepseek-v2:latest")
    return RetrievalQA.from_chain_type(llm, retriever=retriever, return_source_documents=True)

qa_chain = create_qa_chain()

# --- Serve PWA static assets ---
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/manifest.json")
def manifest():
    return send_from_directory(app.static_folder, "manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(app.static_folder, "service-worker.js")

@app.route("/icons/<path:filename>")
def icons(filename):
    return send_from_directory(os.path.join(app.static_folder, "icons"), filename)

# --- RAG Chatbot logic ---
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query is empty"}), 400

    result = qa_chain.invoke({"query": query})
    answer = result["result"]

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    top_docs = qa_chain.retriever.invoke(query)

    if top_docs:
        query_vec = np.array(embeddings.embed_query(query)).reshape(1, -1)
        doc_vec = np.array(embeddings.embed_documents([top_docs[0].page_content])[0]).reshape(1, -1)
        similarity = cosine_similarity(query_vec, doc_vec)[0][0]
        confidence_score = max(0.0, min(similarity, 1.0)) * 100
    else:
        confidence_score = 50.0

    sentiment = analyze_sentiment(answer)

    return jsonify({
        "answer": answer,
        "confidence": round(confidence_score, 2),
        "sentiment": sentiment
    })

# --- Feedback API ---
@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT, response TEXT, sentiment TEXT,
            confidence REAL, feedback TEXT, email TEXT
        )
    """)
    c.execute("INSERT INTO feedback (query, response, sentiment, confidence, feedback, email) VALUES (?, ?, ?, ?, ?, ?)",
              (data["query"], data["response"], data["sentiment"], data["confidence"], data["feedback"], data.get("email")))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# --- Catch-all fallback for SPA routing ---
@app.errorhandler(404)
def fallback(e):
    return send_from_directory(app.static_folder, "index.html")

# --- Run the server ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
