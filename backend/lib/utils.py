import sqlite3
from pathlib import Path

# Use a single DB file under the repo so examples and utils agree
DB_PATH = Path(__file__).resolve().parent / "data.db"


def connect_db():
    conn = sqlite3.connect(str(DB_PATH))
    # conn.row_factory = sqlite3.Row # access columns by name (e.g., row['name'])
    return conn


def ensure_tables():
    """Create the users and items tables if they don't exist."""
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT CHECK(type IN ('LOST', 'FOUND')),
                status TEXT DEFAULT 'OPEN',
                category TEXT,
                description TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        conn.commit()