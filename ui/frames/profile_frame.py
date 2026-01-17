"""
Profile frame displaying user information.
"""
import customtkinter as ctk
import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING
from ui.styles import (
    create_header_frame, create_sidebar_frame, create_nav_button,
    CARD_PROFILE
)

if TYPE_CHECKING:
    from ui.app import App


class ProfileFrame(ctk.CTkFrame):
    """Frame for displaying user profile information."""
    
    def __init__(self, parent: "App"):
        """
        Initialize the profile frame.
        
        Args:
            parent: The main App instance
        """
        super().__init__(parent)
        self.parent = parent
        self.place(relwidth=1, relheight=1)
        
        # Header and sidebar
        create_header_frame(self)
        create_sidebar_frame(self)
        
        # Profile card
        ctk.CTkFrame(
            self,
            width=600,
            height=300,
            fg_color=CARD_PROFILE,
            corner_radius=20
        ).place(x=300, y=150)
        
        # Profile labels
        self._create_profile_labels()
        
        # Navigation buttons
        self._create_nav_buttons()
    
    def _create_profile_labels(self) -> None:
        """Create profile information labels."""
        # Header name
        self.header_name_label = ctk.CTkLabel(
            self,
            font=("Poppins", 25, "bold"),
            text="Loading...",
            fg_color=CARD_PROFILE
        )
        self.header_name_label.place(x=320, y=230)
        
        # Field labels
        ctk.CTkLabel(
            self,
            font=("Poppins", 15, "bold"),
            text="Name:",
            fg_color=CARD_PROFILE
        ).place(x=320, y=300)
        
        ctk.CTkLabel(
            self,
            font=("Poppins", 15, "bold"),
            text="Email:",
            fg_color=CARD_PROFILE
        ).place(x=320, y=340)
        
        ctk.CTkLabel(
            self,
            font=("Poppins", 15, "bold"),
            text="Password:",
            fg_color=CARD_PROFILE
        ).place(x=320, y=380)
        
        # Value labels
        self.name_value = ctk.CTkLabel(
            self,
            font=("Poppins", 15),
            text="...",
            fg_color=CARD_PROFILE
        )
        self.name_value.place(x=450, y=300)
        
        self.email_value = ctk.CTkLabel(
            self,
            font=("Poppins", 15),
            text="...",
            fg_color=CARD_PROFILE
        )
        self.email_value.place(x=450, y=340)
        
        self.pass_value = ctk.CTkLabel(
            self,
            font=("Poppins", 15),
            text="********",
            fg_color=CARD_PROFILE
        )
        self.pass_value.place(x=450, y=380)
        
        # Change password button
        ctk.CTkButton(
            self,
            text="Change Password",
            font=("Poppins", 12),
            width=150,
            height=30,
            fg_color="#2b9348",
            command=self.change_password
        ).place(x=750, y=380)
    
    def _create_nav_buttons(self) -> None:
        """Create navigation menu buttons."""
        create_nav_button(
            self,
            "MENU",
            command=lambda: self.parent.show_frame(self.parent.login_frame),
            y_position=0,
            height=70
        ).place(x=0, y=0)
        
        create_nav_button(
            self,
            "User Profile",
            command=lambda: self.parent.show_frame(self.parent.profile_frame)
        ).place(x=0, y=71)
        
        create_nav_button(
            self,
            "Dashboard",
            command=lambda: self.parent.show_frame(self.parent.dashboard_frame)
        ).place(x=0, y=122)
        
        create_nav_button(
            self,
            "View Lost Items",
            command=lambda: self.parent.show_frame(self.parent.view_items_frame)
        ).place(x=0, y=173)
        
        create_nav_button(
            self,
            "My Items",
            command=lambda: self.parent.show_frame(self.parent.my_items_frame)
        ).place(x=0, y=224)
        
        create_nav_button(
            self,
            "Report Missing Items",
            command=lambda: self.parent.show_frame(self.parent.report_item_frame)
        ).place(x=0, y=275)
    
    def load_data(self) -> None:
        """Load and display current user information."""
        current_id = self.parent.current_user_id
        
        if not current_id:
            self.header_name_label.configure(text="Guest")
            self.name_value.configure(text="Not logged in")
            self.email_value.configure(text="Not logged in")
            return
        
        try:
            from database.queries import get_user_info
            
            user_info = get_user_info(current_id)
            
            if user_info:
                username, email = user_info
                self.header_name_label.configure(text=username)
                self.name_value.configure(text=username)
                self.email_value.configure(text=email)
            else:
                self.header_name_label.configure(text="User not found")
                self.name_value.configure(text="N/A")
                self.email_value.configure(text="N/A")
        except Exception as e:
            print(f"Error loading profile: {e}")
            self.header_name_label.configure(text="Error")
            self.name_value.configure(text="Failed to load")
            self.email_value.configure(text="Failed to load")
    
    def change_password(self) -> None:
        """Open password change dialog."""
        current_id = self.parent.current_user_id
        
        if not current_id:
            messagebox.showerror("Error", "Please login first.")
            return
        
        # Create password change dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Change Password")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        
        # Old password
        ctk.CTkLabel(
            dialog,
            text="Current Password:",
            font=("Poppins", 12, "bold")
        ).place(x=20, y=20)
        
        old_pass_entry = ctk.CTkEntry(
            dialog,
            width=350,
            height=30,
            show="*"
        )
        old_pass_entry.place(x=20, y=50)
        
        # New password
        ctk.CTkLabel(
            dialog,
            text="New Password:",
            font=("Poppins", 12, "bold")
        ).place(x=20, y=90)
        
        new_pass_entry = ctk.CTkEntry(
            dialog,
            width=350,
            height=30,
            show="*"
        )
        new_pass_entry.place(x=20, y=120)
        
        # Confirm new password
        ctk.CTkLabel(
            dialog,
            text="Confirm New Password:",
            font=("Poppins", 12, "bold")
        ).place(x=20, y=160)
        
        confirm_pass_entry = ctk.CTkEntry(
            dialog,
            width=350,
            height=30,
            show="*"
        )
        confirm_pass_entry.place(x=20, y=190)
        
        def save_password():
            old_pass = old_pass_entry.get().strip()
            new_pass = new_pass_entry.get().strip()
            confirm_pass = confirm_pass_entry.get().strip()
            
            # Validation
            if not old_pass or not new_pass or not confirm_pass:
                messagebox.showerror("Validation Error", "All fields are required.")
                return
            
            if new_pass != confirm_pass:
                messagebox.showerror("Validation Error", "New passwords do not match.")
                return
            
            if len(new_pass) < 4:
                messagebox.showerror("Validation Error", "Password must be at least 4 characters long.")
                return
            
            try:
                from database.queries import change_password
                
                success = change_password(current_id, old_pass, new_pass)
                
                if success:
                    messagebox.showinfo("Success", "Password changed successfully!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Current password is incorrect.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change password: {str(e)}")
        
        # Buttons
        ctk.CTkButton(
            dialog,
            text="Change Password",
            fg_color="#2b9348",
            width=150,
            command=save_password
        ).place(x=50, y=220)
        
        ctk.CTkButton(
            dialog,
            text="Cancel",
            fg_color="#6c757d",
            width=150,
            command=dialog.destroy
        ).place(x=220, y=220)

