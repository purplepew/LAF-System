from ..utils import connect_db

def get_all_items():
    """Fetch all items including the ID."""
    with connect_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                items.id,             -- [0] ID
                items.item_name,      -- [1] Name
                items.landmark,       -- [2] Landmark
                items.date_found,     -- [3] Date
                items.time_found,     -- [4] Time
                users.username,       -- [5] User (Joined)
                items.type,           -- [6] Type
                items.description,    -- [7] Description
                items.image_path,     -- [8] Image Path
                items.status          -- [9] Status <--- MUST BE HERE
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