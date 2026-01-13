from ..utils import connect_db
import sqlite3

def register_user(username, password, email):
    """Creates a new user account."""
    with connect_db() as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (username, password, email) 
                VALUES (?, ?, ?)
            """, (username, password, email))
            
            conn.commit()
            print(f"User {username} registered successfully!")
            return True
            
        except sqlite3.IntegrityError:
            print("Error: Username already exists.")
            return False
        except Exception as e:
            print(f"Registration error: {e}")
            return False
