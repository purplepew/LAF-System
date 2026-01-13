from ..utils import connect_db

def get_all_items():
    """Fetch all items and join with users table to get names."""
    with connect_db() as conn:
        cursor = conn.cursor()
        
        # We perform a JOIN to get 'users.name' based on 'items.user_id'
        cursor.execute("""
            SELECT 
                items.item_name, 
                items.landmark, 
                items.date_found, 
                items.time_found, 
                users.username,       
                items.type, 
                items.description 
            FROM items
            JOIN users ON items.user_id = users.id
        """)
        
        return cursor.fetchall()

def get_items_by_type(item_type):
    """Fetch items based on type ('LOST' or 'FOUND')."""
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT item_name, landmark, date_found, time_found, description 
            FROM items 
            WHERE type = ?
        """, (item_type,))
        
        return cursor.fetchall()