"""
Main entry point for the Lost and Found System application.
Initializes the database and starts the GUI application.
"""
import customtkinter as ctk
from database.db_manager import ensure_tables
from ui.app import App


def main() -> None:
    """Initialize database and start the application."""
    # Ensure database tables exist
    try:
        ensure_tables()
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return
    
    # Configure customtkinter
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    # Create and run the application
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

