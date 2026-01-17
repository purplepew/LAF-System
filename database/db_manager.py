"""
Database connection and table management module.
Handles SQLite connection and ensures all required tables exist.
"""
import sqlite3
from pathlib import Path
from typing import Optional


# Database file path - stored in database directory
DB_PATH = Path(__file__).resolve().parent / "data.db"


def connect_db() -> sqlite3.Connection:
    """
    Create and return a database connection.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(str(DB_PATH))
    return conn


def ensure_tables() -> None:
    """
    Create the users and items tables if they don't exist.
    Ensures the database schema is properly initialized.
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()

            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            """)

            # Create items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    item_name TEXT,
                    landmark TEXT,
                    date_found TEXT,
                    time_found TEXT,
                    type TEXT CHECK(type IN ('LOST', 'FOUND')),
                    status TEXT DEFAULT 'OPEN',
                    category TEXT,
                    description TEXT,
                    image_path TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)

            conn.commit()
    except sqlite3.Error as e:
        raise Exception(f"Database initialization error: {e}")

