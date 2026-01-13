from ..utils import connect_db

def get_all_users(batch_size=5):
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")

        users = cursor.fetchmany(batch_size)

        return users


def login_user(username, password):
    """Checks credentials and returns User ID if valid, else None."""
    with connect_db() as conn:
        cursor = conn.cursor()
        
        # specific query to check for a match
        cursor.execute("""
            SELECT id FROM users 
            WHERE username = ? AND password = ?
        """, (username, password))
        
        result = cursor.fetchone()
        
        if result:
            return result[0] # Return the User ID
        else:
            return None      # Login failed

def get_user_info(user_id):
    """Fetches username and email for a specific user ID."""
    with connect_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT username, email FROM users WHERE id = ?
        """, (user_id,))
        
        return cursor.fetchone() # Returns a tuple: (username, email)