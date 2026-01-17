from ..utils import connect_db

from ..utils import connect_db

def seed_items():
    """Inserts 4 dummy items into the database."""
    
    # Data structure: (user_id, item_name, landmark, date_found, time_found, type, description)
    items_to_add = [
        (1, "Black Backpack", "Main Library", "13/01/2026", "09:30 AM", "LOST", "Black JanSport bag with a laptop inside."),
        (1, "Silver Water Bottle", "Gymnasium", "12/01/2026", "04:15 PM", "LOST", "Has a sticker on the side."),
        (1, "Honda Car Keys", "Parking Lot A", "11/01/2026", "08:00 AM", "FOUND", "Found near the south entrance."),
        (1, "Calculus Textbook", "Room 304", "10/01/2026", "02:00 PM", "FOUND", "Left on the second row desk.")
    ]

    with connect_db() as conn:
        cursor = conn.cursor()

        # We use executemany to insert multiple rows at once
        cursor.executemany("""
            INSERT INTO items (
                user_id, item_name, landmark, date_found, time_found, type, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, items_to_add)

        conn.commit()
        print("Successfully added 4 test items.")

def create_new_item(user_id, item_name, landmark, date_found, time_found, item_type, description, image_path=None):
    with connect_db() as conn:
        cursor = conn.cursor()

        # Added image_path column
        cursor.execute("""
            INSERT INTO items (
                user_id, 
                item_name, 
                landmark, 
                date_found, 
                time_found, 
                type, 
                description,
                image_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, item_name, landmark, date_found, time_found, item_type, description, image_path))
        
        conn.commit()

def mark_item_as_claimed(item_id):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE items SET status = 'CLAIMED' WHERE id = ?", (item_id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error claiming item: {e}")
        return False