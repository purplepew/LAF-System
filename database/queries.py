"""
Database query module.
Contains all SQL SELECT, INSERT, and UPDATE operations.
All database queries should be centralized here.
"""
import sqlite3
from typing import Optional, Tuple, List
from database.db_manager import connect_db


def login_user(username: str, password: str) -> Optional[int]:
    """
    Authenticate user credentials and return user ID if valid.
    
    Args:
        username: Username to authenticate
        password: Password to authenticate
        
    Returns:
        User ID if credentials are valid, None otherwise
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id FROM users 
                WHERE username = ? AND password = ?
            """, (username, password))
            result = cursor.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        raise Exception(f"Login query error: {e}")


def get_user_info(user_id: int) -> Optional[Tuple[str, str]]:
    """
    Fetch username and email for a specific user ID.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Tuple of (username, email) if found, None otherwise
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username, email FROM users WHERE id = ?
            """, (user_id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        raise Exception(f"Get user info error: {e}")


def register_user(username: str, password: str, email: str) -> bool:
    """
    Create a new user account.
    
    Args:
        username: Username for the new account
        password: Password for the new account
        email: Email address for the new account
        
    Returns:
        True if registration successful, False if username already exists
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, email) 
                VALUES (?, ?, ?)
            """, (username, password, email))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    except sqlite3.Error as e:
        raise Exception(f"Registration error: {e}")


def get_all_items() -> List[Tuple]:
    """
    Fetch all items with user information joined.
    
    Returns:
        List of tuples containing item data:
        (id, item_name, landmark, date_found, time_found, username, 
         type, description, image_path, status)
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    items.id,
                    items.item_name,
                    items.landmark,
                    items.date_found,
                    items.time_found,
                    users.username,
                    items.type,
                    items.description,
                    items.image_path,
                    items.status
                FROM items
                JOIN users ON items.user_id = users.id
                ORDER BY items.id DESC
            """)
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise Exception(f"Get all items error: {e}")


def get_dashboard_stats(user_id: int) -> Tuple[int, int, int]:
    """
    Get dashboard statistics for a user.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Tuple of (your_items, total_items, pending)
        - your_items: All items reported by this user (regardless of status)
        - total_items: All items in the system (regardless of status)
        - pending: All items that are still OPEN
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            
            # Your items (all items reported by this user)
            cursor.execute("""
                SELECT COUNT(*) FROM items WHERE user_id = ?
            """, (user_id,))
            your_items = cursor.fetchone()[0]
            
            # Total items (all items in system)
            cursor.execute("""
                SELECT COUNT(*) FROM items
            """)
            total_items = cursor.fetchone()[0]
            
            # Pending items (items with OPEN status)
            cursor.execute("""
                SELECT COUNT(*) FROM items WHERE status = 'OPEN'
            """)
            pending = cursor.fetchone()[0]
            
            return (your_items, total_items, pending)
    except sqlite3.Error as e:
        raise Exception(f"Get dashboard stats error: {e}")


def create_item(
    user_id: int,
    item_name: str,
    landmark: str,
    date_found: str,
    time_found: str,
    item_type: str,
    description: str,
    image_path: Optional[str] = None
) -> bool:
    """
    Create a new lost/found item.
    
    Args:
        user_id: ID of the user reporting the item
        item_name: Name of the item
        landmark: Location where item was found/lost
        date_found: Date when item was found/lost
        time_found: Time when item was found/lost
        item_type: Either 'LOST' or 'FOUND'
        description: Description of the item
        image_path: Optional path to item image
        
    Returns:
        True if item created successfully
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO items (
                    user_id, item_name, landmark, date_found, 
                    time_found, type, description, image_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, item_name, landmark, date_found, 
                  time_found, item_type, description, image_path))
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise Exception(f"Create item error: {e}")


def update_item_status(item_id: int, status: str) -> bool:
    """
    Update the status of an item (e.g., mark as CLAIMED).
    
    Args:
        item_id: ID of the item to update
        status: New status (e.g., 'CLAIMED', 'OPEN')
        
    Returns:
        True if update successful
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE items SET status = ? WHERE id = ?
            """, (status, item_id))
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise Exception(f"Update item status error: {e}")

