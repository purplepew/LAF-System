from ..utils import connect_db

def create_new_user(name, email):
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (name, email) values (?, ?)
        """, [name, email])
