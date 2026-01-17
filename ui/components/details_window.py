"""
Details window component for displaying item details and claiming items.
"""
import customtkinter as ctk
from PIL import Image
import os
import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.frames.view_items_frame import ViewItemsFrame


class DetailsWindow(ctk.CTkToplevel):
    """Popup window displaying detailed item information with image."""
    
    def __init__(self, parent: "ViewItemsFrame", item_data: tuple):
        """
        Initialize the details window.
        
        Args:
            parent: The parent ViewItemsFrame instance
            item_data: Tuple containing item data from database
                       (id, name, landmark, date, time, username, type, desc, image, status)
        """
        super().__init__(parent)
        self.title("Item Details")
        self.geometry("400x600")
        self.resizable(False, False)
        
        self.item_data = item_data
        self.parent = parent
        
        # Image display
        self._create_image_display()
        
        # Details display
        self._create_details_display()
        
        # Action buttons
        self._create_buttons()
    
    def _create_image_display(self) -> None:
        """Create the image display label."""
        self.image_label = ctk.CTkLabel(
            self,
            text="No Image",
            width=300,
            height=200,
            fg_color="gray"
        )
        self.image_label.pack(pady=20)
        
        # Try to load image
        # item_data structure: (id, name, landmark, date, time, username, type, desc, image, status, category)
        img_path = self.item_data[8] if len(self.item_data) > 8 else None
        
        if img_path and os.path.exists(img_path):
            try:
                my_image = ctk.CTkImage(
                    light_image=Image.open(img_path),
                    size=(300, 200)
                )
                self.image_label.configure(image=my_image, text="")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.image_label.configure(text="Image load failed")
    
    def _create_details_display(self) -> None:
        """Create the details display labels."""
        # item_data structure: (id, name, landmark, date, time, username, type, desc, image, status, category)
        item_name = self.item_data[1] if len(self.item_data) > 1 else "Unknown"
        description = self.item_data[7] if len(self.item_data) > 7 else "No description"
        landmark = self.item_data[2] if len(self.item_data) > 2 else "Unknown"
        date = self.item_data[3] if len(self.item_data) > 3 else "Unknown"
        time = self.item_data[4] if len(self.item_data) > 4 else "Unknown"
        status = self.item_data[9] if len(self.item_data) > 9 else "Unknown"
        category = self.item_data[10] if len(self.item_data) > 10 else "Uncategorized"
        
        # Display item information
        ctk.CTkLabel(
            self,
            text=f"Item: {item_name}",
            font=("Poppins", 20, "bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            self,
            text=f"Description: {description}",
            font=("Poppins", 14)
        ).pack(pady=5)
        
        ctk.CTkLabel(
            self,
            text=f"Type: {self.item_data[6] if len(self.item_data) > 6 else 'Unknown'}",
            font=("Poppins", 14)
        ).pack(pady=5)
        
        ctk.CTkLabel(
            self,
            text=f"Location: {landmark}",
            font=("Poppins", 14)
        ).pack(pady=5)
        
        ctk.CTkLabel(
            self,
            text=f"Date: {date} at {time}",
            font=("Poppins", 14)
        ).pack(pady=5)
        
        ctk.CTkLabel(
            self,
            text=f"Category: {category}",
            font=("Poppins", 14)
        ).pack(pady=5)
        
        ctk.CTkLabel(
            self,
            text=f"Status: {status}",
            font=("Poppins", 14, "bold")
        ).pack(pady=5)
    
    def _create_buttons(self) -> None:
        """Create action buttons."""
        # Claim button (only show if status is OPEN)
        status = self.item_data[9] if len(self.item_data) > 9 else "Unknown"
        
        if status == "OPEN":
            ctk.CTkButton(
                self,
                text="Claim Item",
                fg_color="#2b9348",
                command=self.handle_claim
            ).pack(pady=20)
        else:
            ctk.CTkLabel(
                self,
                text="Item already claimed",
                font=("Poppins", 14),
                text_color="gray"
            ).pack(pady=20)
        
        # Close button
        ctk.CTkButton(
            self,
            text="Close",
            fg_color="red",
            command=self.destroy
        ).pack(pady=5)
    
    def handle_claim(self) -> None:
        """Handle item claiming with validation and database update."""
        # item_data structure: (id, name, landmark, date, time, username, type, desc, image, status, category)
        item_id = self.item_data[0]
        
        try:
            from database.queries import update_item_status
            
            success = update_item_status(item_id, "CLAIMED")
            
            if success:
                messagebox.showinfo("Success", "Item claimed successfully!")
                
                # Refresh parent table
                if hasattr(self.parent, 'load_data'):
                    self.parent.load_data()
                
                # Refresh dashboard if it exists
                if hasattr(self.parent.parent, 'dashboard_frame'):
                    if hasattr(self.parent.parent.dashboard_frame, 'load_data'):
                        self.parent.parent.dashboard_frame.load_data()
                
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to claim item.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to claim item: {str(e)}")

