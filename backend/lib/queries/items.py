from ..utils import connect_db

def get_all_items():
    """Fetch all items from the database."""
    with connect_db() as conn:
        cursor = conn.cursor()
        
        # We select specific columns to match your Treeview (Table)
        cursor.execute("""
            SELECT item_name, landmark, date_found, time_found, type, description 
            FROM items
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