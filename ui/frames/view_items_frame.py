"""
View items frame displaying all lost/found items in a table.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING, Dict
from ui.styles import create_header_frame, create_sidebar_frame, create_nav_button, create_button

if TYPE_CHECKING:
    from ui.app import App


class ViewItemsFrame(ctk.CTkFrame):
    """Frame for viewing all lost/found items in a table."""
    
    def __init__(self, parent: "App"):
        """
        Initialize the view items frame.
        
        Args:
            parent: The main App instance
        """
        super().__init__(parent)
        self.parent = parent
        self.place(relwidth=1, relheight=1)
        
        # Dictionary to store full item data (hidden from table)
        self.item_map: Dict[int, tuple] = {}
        
        # Header and sidebar
        create_header_frame(self)
        create_sidebar_frame(self)
        
        # Title
        ctk.CTkLabel(
            self,
            font=("Poppins", 15, "bold"),
            text="View Lost Items",
            fg_color="transparent"
        ).place(x=220, y=85)
        
        # Table
        self._create_table()
        
        # View details button
        create_button(
            self,
            "View Selected Details & Image",
            command=self.open_details,
            fg_color="#0077b6",
            width=200
        ).place(x=500, y=450)
        
        # Double-click to open details
        self.tree.bind("<Double-1>", lambda event: self.open_details())
        
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
        
        columns = ("Item Name", "Landmark", "Date Found", "Time Found", "Reported By", "Status")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=15
        )
        self.tree.place(x=210, y=135)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        
        scroll_y = tk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        scroll_y.place(x=975, y=135, height=300)
        self.tree.configure(yscrollcommand=scroll_y.set)
    
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
            "Report Missing Items",
            command=lambda: self.parent.show_frame(self.parent.report_item_frame)
        ).place(x=0, y=224)
    
    def load_data(self) -> None:
        """Load and refresh items table data."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.item_map = {}  # Reset map
        
        try:
            from database.queries import get_all_items
            
            items = get_all_items()
            
            for index, item in enumerate(items):
                # item structure: (id, name, landmark, date, time, username, type, desc, image, status)
                row_values = (
                    item[1],  # name
                    item[2],  # landmark
                    item[3],  # date
                    item[4],  # time
                    item[5],  # username
                    item[9] if len(item) > 9 else "Unknown"  # status
                )
                
                self.tree.insert("", "end", iid=index, values=row_values)
                self.item_map[index] = item
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load items: {str(e)}")
    
    def open_details(self) -> None:
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

