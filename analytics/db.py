import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            response TEXT,
            sentiment TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_interaction(query, response, sentiment):
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO query_log (query, response, sentiment, timestamp)
        VALUES (?, ?, ?, ?)
    """, (query, response, sentiment, datetime.now().isoformat()))
    conn.commit()
    conn.close()
