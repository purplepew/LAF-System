"""
Signup frame for user registration.
"""
import customtkinter as ctk
import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING
from ui.styles import create_header_label, create_title_label, create_entry, create_button

if TYPE_CHECKING:
    from ui.app import App


class SignupFrame(ctk.CTkFrame):
    """Frame for user registration functionality."""
    
    def __init__(self, parent: "App"):
        """
        Initialize the signup frame.
        
        Args:
            parent: The main App instance
        """
        super().__init__(parent)
        self.parent = parent
        self.place(relwidth=1, relheight=1)
        
        # Header
        create_header_label(self, "Lost and Found System").pack(pady=50)
        create_title_label(self, "Create an Account", font_size=23).pack()
        
        # Input fields
        self.username_entry = create_entry(self, "Username")
        self.username_entry.pack(pady=8)
        
        self.password_entry = create_entry(self, "Password", show="*")
        self.password_entry.pack(pady=8)
        
        self.email_entry = create_entry(self, "Email")
        self.email_entry.pack(pady=8)
        
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
            "Register",
            command=self.handle_register
        ).pack(pady=10)
        
        create_button(
            self,
            "Back to Login",
            command=lambda: parent.show_frame(parent.login_frame)
        ).pack()
    
    def handle_register(self) -> None:
        """Handle registration with input validation."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()
        
        # Input validation
        if not username or not password or not email:
            messagebox.showerror("Validation Error", "All fields are required.")
            self.error_label.configure(text="All fields are required.")
            return
        
        # Basic email validation
        if "@" not in email or "." not in email:
            messagebox.showerror("Validation Error", "Please enter a valid email address.")
            self.error_label.configure(text="Please enter a valid email address.")
            return
        
        try:
            from database.queries import register_user
            
            success = register_user(username, password, email)
            
            if success:
                messagebox.showinfo("Success", "Account created successfully! Redirecting to login...")
                
                # Clear inputs
                self.username_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                self.email_entry.delete(0, 'end')
                self.error_label.configure(text="")
                
                # Navigate to login
                self.parent.show_frame(self.parent.login_frame)
            else:
                error_msg = "Username already exists. Please choose a different username."
                self.error_label.configure(text=error_msg)
                messagebox.showerror("Registration Failed", error_msg)
        except Exception as e:
            error_msg = f"Registration error: {str(e)}"
            self.error_label.configure(text=error_msg)
            messagebox.showerror("Error", error_msg)

