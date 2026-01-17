"""
Edit item window component for editing existing items.
"""
import customtkinter as ctk
from tkinter import filedialog
import os
import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ui.frames.my_items_frame import MyItemsFrame


class EditItemWindow(ctk.CTkToplevel):
    """Popup window for editing item details."""
    
    def __init__(self, parent: "MyItemsFrame", item_data: tuple):
        """
        Initialize the edit item window.
        
        Args:
            parent: The parent MyItemsFrame instance
            item_data: Tuple containing item data from database
        """
        super().__init__(parent)
        self.title("Edit Item")
        self.geometry("500x600")
        self.resizable(False, False)
        
        self.item_data = item_data
        self.parent = parent
        self.image_path: Optional[str] = None
        
        # item_data structure: (id, name, landmark, date, time, username, type, desc, image, status, category)
        self.item_id = item_data[0]
        
        # Form fields
        self._create_form_fields()
        
        # Buttons
        self._create_buttons()
    
    def _create_form_fields(self) -> None:
        """Create form input fields pre-filled with item data."""
        # Item Name
        ctk.CTkLabel(self, text="Item Name:", font=("Poppins", 12, "bold")).place(x=20, y=20)
        self.name_entry = ctk.CTkEntry(self, width=450, height=30)
        self.name_entry.insert(0, self.item_data[1])
        self.name_entry.place(x=20, y=50)
        
        # Landmark
        ctk.CTkLabel(self, text="Landmark:", font=("Poppins", 12, "bold")).place(x=20, y=90)
        self.landmark_entry = ctk.CTkEntry(self, width=450, height=30)
        self.landmark_entry.insert(0, self.item_data[2])
        self.landmark_entry.place(x=20, y=120)
        
        # Date Found
        ctk.CTkLabel(self, text="Date Found:", font=("Poppins", 12, "bold")).place(x=20, y=160)
        self.date_entry = ctk.CTkEntry(self, width=450, height=30)
        self.date_entry.insert(0, self.item_data[3])
        self.date_entry.place(x=20, y=190)
        
        # Time Found
        ctk.CTkLabel(self, text="Time Found:", font=("Poppins", 12, "bold")).place(x=20, y=230)
        self.time_entry = ctk.CTkEntry(self, width=450, height=30)
        self.time_entry.insert(0, self.item_data[4])
        self.time_entry.place(x=20, y=260)
        
        # Description
        ctk.CTkLabel(self, text="Description:", font=("Poppins", 12, "bold")).place(x=20, y=300)
        self.desc_entry = ctk.CTkEntry(self, width=450, height=30)
        self.desc_entry.insert(0, self.item_data[7] if len(self.item_data) > 7 else "")
        self.desc_entry.place(x=20, y=330)
        
        # Category
        ctk.CTkLabel(self, text="Category:", font=("Poppins", 12, "bold")).place(x=20, y=370)
        self.category_entry = ctk.CTkComboBox(
            self,
            values=["Electronics", "Clothing", "Documents", "Accessories", "Books", "Other"],
            width=450,
            height=30
        )
        category = self.item_data[10] if len(self.item_data) > 10 else "Other"
        self.category_entry.set(category if category else "Other")
        self.category_entry.place(x=20, y=400)
        
        # Image
        ctk.CTkLabel(self, text="Image:", font=("Poppins", 12, "bold")).place(x=20, y=440)
        ctk.CTkButton(
            self,
            text="Browse",
            width=100,
            height=30,
            command=self.browse_image
        ).place(x=20, y=470)
        
        self.file_label = ctk.CTkLabel(
            self,
            text=os.path.basename(self.item_data[8]) if len(self.item_data) > 8 and self.item_data[8] else "No image",
            font=("Poppins", 10)
        )
        self.file_label.place(x=130, y=475)
    
    def _create_buttons(self) -> None:
        """Create action buttons."""
        ctk.CTkButton(
            self,
            text="Save Changes",
            fg_color="#2b9348",
            width=200,
            command=self.save_changes
        ).place(x=100, y=520)
        
        ctk.CTkButton(
            self,
            text="Cancel",
            fg_color="#6c757d",
            width=200,
            command=self.destroy
        ).place(x=310, y=520)
    
    def browse_image(self) -> None:
        """Open file dialog to select an image."""
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if filename:
            self.image_path = filename
            self.file_label.configure(text=os.path.basename(filename))
    
    def save_changes(self) -> None:
        """Save edited item data."""
        # Get form values
        i_name = self.name_entry.get().strip()
        i_landmark = self.landmark_entry.get().strip()
        i_date = self.date_entry.get().strip()
        i_time = self.time_entry.get().strip()
        i_desc = self.desc_entry.get().strip()
        category = self.category_entry.get()
        
        # Validation
        if not i_name or not i_landmark or not i_date or not i_time:
            messagebox.showerror("Validation Error", "Please fill in all required fields.")
            return
        
        try:
            from database.queries import update_item
            
            success = update_item(
                self.item_id,
                i_name,
                i_landmark,
                i_date,
                i_time,
                i_desc,
                category,
                self.image_path if self.image_path else None
            )
            
            if success:
                messagebox.showinfo("Success", "Item updated successfully!")
                self.parent.load_data()  # Refresh parent table
                
                # Refresh dashboard if it exists
                if hasattr(self.parent.parent, 'dashboard_frame'):
                    if hasattr(self.parent.parent.dashboard_frame, 'load_data'):
                        self.parent.parent.dashboard_frame.load_data()
                
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to update item.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item: {str(e)}")

