from ..utils import connect_db

def get_all_users(batch_size=5):
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")

        users = cursor.fetchmany(batch_size)

        return users
