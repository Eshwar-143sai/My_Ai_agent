import sqlite3
import os

DB_PATH = "feedback.db"

def init_db():
    """Initializes the SQLite database required for RLHF feedback loops."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_feedback(conversation_id: str, rating: int, comment: str):
    """Inserts a new feedback rating into the SQLite DB."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (conversation_id, rating, comment)
        VALUES (?, ?, ?)
    ''', (conversation_id, rating, comment))
    conn.commit()
    conn.close()
