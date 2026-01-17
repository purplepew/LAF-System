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


def get_user_info(user_id: int) -> Optional[Tuple[str, str, str, str]]:
    """
    Fetch username, email, first_name, and last_name for a specific user ID.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Tuple of (username, email, first_name, last_name) if found, None otherwise
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username, email, first_name, last_name FROM users WHERE id = ?
            """, (user_id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        raise Exception(f"Get user info error: {e}")


def register_user(username: str, password: str, email: str, first_name: str = "", last_name: str = "") -> bool:
    """
    Create a new user account.
    
    Args:
        username: Username for the new account
        password: Password for the new account
        email: Email address for the new account
        first_name: First name of the user
        last_name: Last name of the user
        
    Returns:
        True if registration successful, False if username already exists
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, email, first_name, last_name) 
                VALUES (?, ?, ?, ?, ?)
            """, (username, password, email, first_name, last_name))
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
         type, description, image_path, status, category)
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
                    items.status,
                    items.category
                FROM items
                JOIN users ON items.user_id = users.id
                ORDER BY items.id DESC
            """)
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise Exception(f"Get all items error: {e}")


def search_items(
    search_term: str = "",
    status_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    category_filter: Optional[str] = None
) -> List[Tuple]:
    """
    Search and filter items based on various criteria.
    
    Args:
        search_term: Search in item name, description, or landmark
        status_filter: Filter by status ('OPEN', 'CLAIMED', or None for all)
        type_filter: Filter by type ('LOST', 'FOUND', or None for all)
        category_filter: Filter by category (or None for all)
        
    Returns:
        List of tuples containing filtered item data
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            
            query = """
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
                    items.status,
                    items.category
                FROM items
                JOIN users ON items.user_id = users.id
                WHERE 1=1
            """
            params = []
            
            # Search term filter
            if search_term:
                query += " AND (items.item_name LIKE ? OR items.description LIKE ? OR items.landmark LIKE ?)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern, search_pattern])
            
            # Status filter
            if status_filter:
                query += " AND items.status = ?"
                params.append(status_filter)
            
            # Type filter
            if type_filter:
                query += " AND items.type = ?"
                params.append(type_filter)
            
            # Category filter
            if category_filter:
                query += " AND items.category = ?"
                params.append(category_filter)
            
            query += " ORDER BY items.id DESC"
            
            cursor.execute(query, params)
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise Exception(f"Search items error: {e}")


def get_user_items(user_id: int) -> List[Tuple]:
    """
    Fetch all items reported by a specific user.
    
    Args:
        user_id: The user's ID
        
    Returns:
        List of tuples containing item data
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
                    items.status,
                    items.category
                FROM items
                JOIN users ON items.user_id = users.id
                WHERE items.user_id = ?
                ORDER BY items.id DESC
            """, (user_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise Exception(f"Get user items error: {e}")


def get_item_by_id(item_id: int) -> Optional[Tuple]:
    """
    Fetch a single item by its ID.
    
    Args:
        item_id: The item's ID
        
    Returns:
        Tuple containing item data or None if not found
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
                    items.status,
                    items.category,
                    items.user_id
                FROM items
                JOIN users ON items.user_id = users.id
                WHERE items.id = ?
            """, (item_id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        raise Exception(f"Get item by id error: {e}")


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
    image_path: Optional[str] = None,
    category: Optional[str] = None
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
        category: Optional category of the item
        
    Returns:
        True if item created successfully
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO items (
                    user_id, item_name, landmark, date_found, 
                    time_found, type, description, image_path, category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, item_name, landmark, date_found, 
                  time_found, item_type, description, image_path, category))
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise Exception(f"Create item error: {e}")


def update_item(
    item_id: int,
    item_name: str,
    landmark: str,
    date_found: str,
    time_found: str,
    description: str,
    category: Optional[str] = None,
    image_path: Optional[str] = None
) -> bool:
    """
    Update an existing item.
    
    Args:
        item_id: ID of the item to update
        item_name: Updated item name
        landmark: Updated landmark
        date_found: Updated date
        time_found: Updated time
        description: Updated description
        category: Updated category
        image_path: Updated image path (optional)
        
    Returns:
        True if update successful
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            if image_path:
                cursor.execute("""
                    UPDATE items SET 
                        item_name = ?, landmark = ?, date_found = ?,
                        time_found = ?, description = ?, category = ?, image_path = ?
                    WHERE id = ?
                """, (item_name, landmark, date_found, time_found, description, category, image_path, item_id))
            else:
                cursor.execute("""
                    UPDATE items SET 
                        item_name = ?, landmark = ?, date_found = ?,
                        time_found = ?, description = ?, category = ?
                    WHERE id = ?
                """, (item_name, landmark, date_found, time_found, description, category, item_id))
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise Exception(f"Update item error: {e}")


def delete_item(item_id: int) -> bool:
    """
    Delete an item by ID.
    
    Args:
        item_id: ID of the item to delete
        
    Returns:
        True if deletion successful
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise Exception(f"Delete item error: {e}")


def verify_item_ownership(item_id: int, user_id: int) -> bool:
    """
    Verify if a user owns a specific item.
    
    Args:
        item_id: ID of the item
        user_id: ID of the user
        
    Returns:
        True if user owns the item, False otherwise
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM items 
                WHERE id = ? AND user_id = ?
            """, (item_id, user_id))
            result = cursor.fetchone()
            return result[0] > 0 if result else False
    except sqlite3.Error as e:
        raise Exception(f"Verify ownership error: {e}")


def change_password(user_id: int, old_password: str, new_password: str) -> bool:
    """
    Change user password.
    
    Args:
        user_id: ID of the user
        old_password: Current password for verification
        new_password: New password to set
        
    Returns:
        True if password changed successfully, False if old password incorrect
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            # First verify old password
            cursor.execute("""
                SELECT id FROM users 
                WHERE id = ? AND password = ?
            """, (user_id, old_password))
            
            if not cursor.fetchone():
                return False  # Old password incorrect
            
            # Update password
            cursor.execute("""
                UPDATE users SET password = ? WHERE id = ?
            """, (new_password, user_id))
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise Exception(f"Change password error: {e}")


def get_all_categories() -> List[str]:
    """
    Get all unique categories from items.
    
    Returns:
        List of unique category names
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT category FROM items 
                WHERE category IS NOT NULL AND category != ''
                ORDER BY category
            """)
            return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        raise Exception(f"Get categories error: {e}")


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

