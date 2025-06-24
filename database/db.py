import sqlite3
from config import DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id TEXT,
                name TEXT,
                last_symptom TEXT
            )
        """)
        conn.commit()

def store_symptom(telegram_id, name, symptom):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (telegram_id, name, last_symptom)
            VALUES (?, ?, ?)
        """, (telegram_id, name, symptom))
        conn.commit()

def get_last_symptom(telegram_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT last_symptom FROM users WHERE telegram_id = ?", (telegram_id,))
        row = cursor.fetchone()
        return row[0] if row else None

