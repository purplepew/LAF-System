"""
My Items frame displaying items reported by the current user.
Includes edit and delete functionality.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING, Dict
from ui.styles import (
    create_header_frame, create_sidebar_frame, create_nav_button, create_button,
    create_menu_label, create_logout_button
)

if TYPE_CHECKING:
    from ui.app import App


class MyItemsFrame(ctk.CTkFrame):
    """Frame for viewing and managing user's own reported items."""
    
    def __init__(self, parent: "App"):
        """
        Initialize the my items frame.
        
        Args:
            parent: The main App instance
        """
        super().__init__(parent)
        self.parent = parent
        self.place(relwidth=1, relheight=1)
        
        # Dictionary to store full item data
        self.item_map: Dict[int, tuple] = {}
        
        # Header and sidebar
        create_header_frame(self)
        create_sidebar_frame(self)
        
        # Title
        ctk.CTkLabel(
            self,
            font=("Poppins", 15, "bold"),
            text="My Reported Items",
            fg_color="transparent"
        ).place(x=220, y=85)
        
        # Table
        self._create_table()
        
        # Action buttons
        create_button(
            self,
            "View Details",
            command=self.view_details,
            fg_color="#0077b6",
            width=150
        ).place(x=400, y=450)
        
        create_button(
            self,
            "Edit Item",
            command=self.edit_item,
            fg_color="#2b9348",
            width=150
        ).place(x=560, y=450)
        
        create_button(
            self,
            "Delete Item",
            command=self.delete_item,
            fg_color="#dc3545",
            width=150
        ).place(x=720, y=450)
        
        # Double-click to view details
        self.tree.bind("<Double-1>", lambda event: self.view_details())
        
        # Navigation buttons
        self._create_nav_buttons()
    
    def _create_table(self) -> None:
        """Create the items table."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview.Heading",
            background="#2b9348",
            font=("Poppins", 10, "bold"),
            foreground="white"
        )
        
        columns = ("Item Name", "Type", "Landmark", "Date Found", "Time Found", "Status", "Category")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=15
        )
        self.tree.place(x=210, y=135)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Item Name":
                self.tree.column(col, width=150)
            elif col == "Type":
                self.tree.column(col, width=80)
            else:
                self.tree.column(col, width=120)
        
        scroll_y = tk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        scroll_y.place(x=1175, y=135, height=300)
        self.tree.configure(yscrollcommand=scroll_y.set)
    
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
    
    def load_data(self) -> None:
        """Load and refresh user's items table data."""
        current_id = self.parent.current_user_id
        
        if not current_id:
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.item_map = {}  # Reset map
        
        try:
            from database.queries import get_user_items
            
            items = get_user_items(current_id)
            
            for index, item in enumerate(items):
                # item structure: (id, name, landmark, date, time, username, type, desc, image, status, category)
                row_values = (
                    item[1],  # name
                    item[6] if len(item) > 6 else "Unknown",  # type
                    item[2],  # landmark
                    item[3],  # date
                    item[4],  # time
                    item[9] if len(item) > 9 else "Unknown",  # status
                    item[10] if len(item) > 10 else "Uncategorized"  # category
                )
                
                self.tree.insert("", "end", iid=index, values=row_values)
                self.item_map[index] = item
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load items: {str(e)}")
    
    def view_details(self) -> None:
        """Open details popup window for selected item."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item first.")
            return
        
        try:
            row_id = int(selected_item[0])
            full_data = self.item_map.get(row_id)
            
            if full_data:
                from ui.components.details_window import DetailsWindow
                DetailsWindow(self, full_data)
            else:
                messagebox.showerror("Error", "Item data not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open details: {str(e)}")
    
    def edit_item(self) -> None:
        """Open edit window for selected item."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item first.")
            return
        
        try:
            row_id = int(selected_item[0])
            full_data = self.item_map.get(row_id)
            
            if not full_data:
                messagebox.showerror("Error", "Item data not found.")
                return
            
            # Verify ownership
            from database.queries import verify_item_ownership
            current_id = self.parent.current_user_id
            
            if not verify_item_ownership(full_data[0], current_id):
                messagebox.showerror("Error", "You can only edit your own items.")
                return
            
            # Open edit window
            from ui.components.edit_item_window import EditItemWindow
            EditItemWindow(self, full_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit item: {str(e)}")
    
    def delete_item(self) -> None:
        """Delete selected item with confirmation."""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item first.")
            return
        
        try:
            row_id = int(selected_item[0])
            full_data = self.item_map.get(row_id)
            
            if not full_data:
                messagebox.showerror("Error", "Item data not found.")
                return
            
            # Verify ownership
            from database.queries import verify_item_ownership, delete_item
            current_id = self.parent.current_user_id
            
            if not verify_item_ownership(full_data[0], current_id):
                messagebox.showerror("Error", "You can only delete your own items.")
                return
            
            # Confirm deletion
            item_name = full_data[1]
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{item_name}'?\nThis action cannot be undone."
            )
            
            if confirm:
                success = delete_item(full_data[0])
                
                if success:
                    messagebox.showinfo("Success", "Item deleted successfully!")
                    self.load_data()  # Refresh table
                    
                    # Refresh dashboard if it exists
                    if hasattr(self.parent.dashboard_frame, 'load_data'):
                        self.parent.dashboard_frame.load_data()
                else:
                    messagebox.showerror("Error", "Failed to delete item.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete item: {str(e)}")

