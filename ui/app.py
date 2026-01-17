"""
Main application class.
Handles frame switching and session state management.
"""
import customtkinter as ctk
from typing import Optional
from ui.frames.login_frame import LoginFrame
from ui.frames.signup_frame import SignupFrame
from ui.frames.dashboard_frame import DashboardFrame
from ui.frames.view_items_frame import ViewItemsFrame
from ui.frames.report_item_frame import ReportItemFrame
from ui.frames.profile_frame import ProfileFrame
from ui.frames.my_items_frame import MyItemsFrame


class App(ctk.CTk):
    """
    Main application class that manages the window and frame switching.
    Maintains session state including current_user_id.
    """
    
    def __init__(self):
        """Initialize the application window and all frames."""
        super().__init__()
        
        self.title("Lost and Found System")
        self.geometry("1200x600")
        self.resizable(False, False)
        
        # Session state - stores current logged-in user ID
        self.current_user_id: Optional[int] = None
        
        # Initialize all frames
        self.login_frame = LoginFrame(self)
        self.signup_frame = SignupFrame(self)
        self.dashboard_frame = DashboardFrame(self)
        self.view_items_frame = ViewItemsFrame(self)
        self.report_item_frame = ReportItemFrame(self)
        self.profile_frame = ProfileFrame(self)
        self.my_items_frame = MyItemsFrame(self)
        
        # Show login frame first
        self.show_frame(self.login_frame)
    
    def show_frame(self, frame: ctk.CTkFrame) -> None:
        """
        Switch to a different frame and refresh its data if needed.
        
        Args:
            frame: The frame to display
        """
        frame.tkraise()
        
        # If frame has load_data method, call it to refresh
        if hasattr(frame, "load_data"):
            try:
                frame.load_data()
            except Exception as e:
                print(f"Error loading frame data: {e}")
    
    def logout(self) -> None:
        """Log out the current user and return to login screen."""
        self.current_user_id = None
        self.show_frame(self.login_frame)

