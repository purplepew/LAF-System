"""
Report item frame for reporting lost/found items.
"""
import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import filedialog
import os
from typing import TYPE_CHECKING, Optional
from ui.styles import (
    create_header_frame, create_sidebar_frame, create_nav_button,
    create_menu_label, create_logout_button,
    create_form_label, create_form_entry, CARD_FORM
)

if TYPE_CHECKING:
    from ui.app import App


class ReportItemFrame(ctk.CTkFrame):
    """Frame for reporting lost/found items."""
    
    def __init__(self, parent: "App"):
        """
        Initialize the report item frame.
        
        Args:
            parent: The main App instance
        """
        super().__init__(parent)
        self.parent = parent
        self.place(relwidth=1, relheight=1)
        
        self.image_path: Optional[str] = None
        
        # Header and sidebar
        create_header_frame(self)
        create_sidebar_frame(self)
        
        # Form background
        ctk.CTkFrame(
            self,
            width=500,
            height=500,
            fg_color=CARD_FORM
        ).place(x=350, y=130)
        
        # Form fields
        self._create_form_fields()
        
        # Navigation buttons
        self._create_nav_buttons()
    
    def _create_form_fields(self) -> None:
        """Create all form input fields."""
        # Item Name
        create_form_label(self, "Item Name", 370, 140).place(x=370, y=140)
        self.name_entry = create_form_entry(self, "Name of Item", 370, 165)
        self.name_entry.place(x=370, y=165)
        
        # Landmark
        create_form_label(self, "Landmark", 370, 200).place(x=370, y=200)
        self.landmark_entry = create_form_entry(self, "Enter Landmark", 370, 225)
        self.landmark_entry.place(x=370, y=225)
        
        # Date Found
        create_form_label(self, "Date Found", 370, 260).place(x=370, y=260)
        self.date_entry = create_form_entry(self, "dd/mm/yyyy", 370, 285)
        self.date_entry.place(x=370, y=285)
        
        # Time Found
        create_form_label(self, "Time Found", 370, 320).place(x=370, y=320)
        self.time_entry = create_form_entry(self, "--:-- --", 370, 345)
        self.time_entry.place(x=370, y=345)
        
        # Description
        create_form_label(self, "Description", 370, 380).place(x=370, y=380)
        self.desc_entry = create_form_entry(self, "e.g. Color: Blue Cotton, with money inside", 370, 405)
        self.desc_entry.place(x=370, y=405)
        
        # Category
        create_form_label(self, "Category", 370, 440).place(x=370, y=440)
        self.category_entry = ctk.CTkComboBox(
            self,
            values=["Electronics", "Clothing", "Documents", "Accessories", "Books", "Other"],
            width=460,
            height=30,
            fg_color="#f8f9fa",
            text_color="black",
            corner_radius=7
        )
        self.category_entry.set("Other")
        self.category_entry.place(x=370, y=465)
        
        # Image section
        create_form_label(self, "Insert Image", 370, 500).place(x=370, y=500)
        
        ctk.CTkButton(
            self,
            text="Browse",
            font=("Poppins", 13, "bold"),
            height=15,
            width=50,
            fg_color="#2b9348",
            corner_radius=5,
            border_width=0,
            command=self.browse_image
        ).place(x=370, y=525)
        
        self.file_label = ctk.CTkLabel(
            self,
            text="No file selected",
            font=("Poppins", 10),
            text_color="black"
        )
        self.file_label.place(x=430, y=530)
        
        # Submit button
        ctk.CTkButton(
            self,
            text="Submit",
            font=("Poppins", 13, "bold"),
            height=15,
            width=460,
            fg_color="#2b9348",
            corner_radius=5,
            border_width=0,
            command=self.submit_form
        ).place(x=370, y=560)
    
    def _create_nav_buttons(self) -> None:
        """Create navigation menu buttons."""
        # Menu label (non-clickable)
        create_menu_label(self).place(x=0, y=0)
        
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
        
        # Logout button
        create_logout_button(
            self,
            command=self.parent.logout
        ).place(x=0, y=326)
    
    def browse_image(self) -> None:
        """Open file dialog to select an image."""
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if filename:
            self.image_path = filename
            self.file_label.configure(text=os.path.basename(filename))
    
    def submit_form(self) -> None:
        """Submit the form with validation and save to database."""
        # Get current user
        current_id = self.parent.current_user_id
        
        if not current_id:
            messagebox.showerror("Error", "Please login first.")
            return
        
        # Get form values
        i_name = self.name_entry.get().strip()
        i_landmark = self.landmark_entry.get().strip()
        i_date = self.date_entry.get().strip()
        i_time = self.time_entry.get().strip()
        i_desc = self.desc_entry.get().strip()
        
        # Validation
        if not i_name or not i_landmark or not i_date or not i_time:
            messagebox.showerror("Validation Error", "Please fill in all required fields (Name, Landmark, Date, Time).")
            return
        
        try:
            from database.queries import create_item
            
            category = self.category_entry.get()
            
            success = create_item(
                current_id,
                i_name,
                i_landmark,
                i_date,
                i_time,
                "LOST",  # Default type
                i_desc,
                self.image_path,
                category
            )
            
            if success:
                messagebox.showinfo("Success", "Item saved successfully!")
                
                # Clear inputs
                self.name_entry.delete(0, 'end')
                self.landmark_entry.delete(0, 'end')
                self.date_entry.delete(0, 'end')
                self.time_entry.delete(0, 'end')
                self.desc_entry.delete(0, 'end')
                self.category_entry.set("Other")
                self.file_label.configure(text="No file selected")
                self.image_path = None
                
                # Refresh dashboard if needed
                if hasattr(self.parent.dashboard_frame, 'load_data'):
                    self.parent.dashboard_frame.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save item: {str(e)}")

