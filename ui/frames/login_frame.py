"""
Login frame for user authentication.
"""
import customtkinter as ctk
import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING
from ui.styles import create_header_label, create_title_label, create_entry, create_button

if TYPE_CHECKING:
    from ui.app import App


class LoginFrame(ctk.CTkFrame):
    """Frame for user login functionality."""
    
    def __init__(self, parent: "App"):
        """
        Initialize the login frame.
        
        Args:
            parent: The main App instance
        """
        super().__init__(parent)
        self.parent = parent
        self.place(relwidth=1, relheight=1)
        
        # Header
        create_header_label(self, "Lost and Found System").pack(pady=50)
        create_title_label(self, "Login").pack()
        
        # Input fields
        self.username_entry = create_entry(self, "Username")
        self.username_entry.pack(pady=8)
        
        self.password_entry = create_entry(self, "Password", show="*")
        self.password_entry.pack(pady=8)
        
        # Error label
        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="red",
            font=("Poppins", 12)
        )
        self.error_label.pack(pady=5)
        
        # Buttons
        create_button(
            self,
            "Login",
            command=self.handle_login,
            fg_color="#2b9348"
        ).pack(pady=8)
        
        create_button(
            self,
            "Sign Up",
            command=lambda: parent.show_frame(parent.signup_frame),
            fg_color="#2b9348"
        ).pack(pady=8)
    
    def handle_login(self) -> None:
        """Handle login button click with validation and authentication."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Input validation
        if not username or not password:
            messagebox.showerror("Validation Error", "Please enter both username and password.")
            self.error_label.configure(text="Please enter both username and password.")
            return
        
        try:
            from database.queries import login_user
            
            user_id = login_user(username, password)
            
            if user_id:
                # Clear error and inputs
                self.error_label.configure(text="")
                self.username_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                
                # Set session state
                self.parent.current_user_id = user_id
                
                # Navigate to dashboard
                self.parent.show_frame(self.parent.dashboard_frame)
            else:
                self.error_label.configure(text="Invalid username or password.")
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except Exception as e:
            error_msg = f"Database error: {str(e)}"
            self.error_label.configure(text=error_msg)
            messagebox.showerror("Error", error_msg)

