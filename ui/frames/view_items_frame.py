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
        
        # Search and filter section
        self._create_search_filters()
        
        # Table
        self._create_table()
        
        # View details button
        create_button(
            self,
            "View Selected Details & Image",
            command=self.open_details,
            fg_color="#0077b6",
            width=200
        ).place(x=600, y=460)
        
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
        
        columns = ("Item Name", "Landmark", "Date Found", "Time Found", "Reported By", "Status", "Category")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=12
        )
        self.tree.place(x=210, y=200)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Item Name":
                self.tree.column(col, width=150)
            elif col == "Category":
                self.tree.column(col, width=120)
            else:
                self.tree.column(col, width=120)
        
        scroll_y = tk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        scroll_y.place(x=1175, y=200, height=250)
        self.tree.configure(yscrollcommand=scroll_y.set)
    
    def _create_search_filters(self) -> None:
        """Create search and filter UI components."""
        # Search entry
        ctk.CTkLabel(
            self,
            font=("Poppins", 12, "bold"),
            text="Search:",
            fg_color="transparent"
        ).place(x=220, y=110)
        
        self.search_entry = ctk.CTkEntry(
            self,
            width=200,
            height=30,
            placeholder_text="Search items..."
        )
        self.search_entry.place(x=280, y=110)
        self.search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())
        
        # Status filter
        ctk.CTkLabel(
            self,
            font=("Poppins", 12, "bold"),
            text="Status:",
            fg_color="transparent"
        ).place(x=500, y=110)
        
        self.status_filter = ctk.CTkComboBox(
            self,
            values=["All", "OPEN", "CLAIMED"],
            width=120,
            height=30,
            command=lambda x: self.apply_filters()
        )
        self.status_filter.set("All")
        self.status_filter.place(x=560, y=110)
        
        # Type filter
        ctk.CTkLabel(
            self,
            font=("Poppins", 12, "bold"),
            text="Type:",
            fg_color="transparent"
        ).place(x=700, y=110)
        
        self.type_filter = ctk.CTkComboBox(
            self,
            values=["All", "LOST", "FOUND"],
            width=120,
            height=30,
            command=lambda x: self.apply_filters()
        )
        self.type_filter.set("All")
        self.type_filter.place(x=750, y=110)
        
        # Category filter
        ctk.CTkLabel(
            self,
            font=("Poppins", 12, "bold"),
            text="Category:",
            fg_color="transparent"
        ).place(x=220, y=150)
        
        self.category_filter = ctk.CTkComboBox(
            self,
            values=["All"],
            width=200,
            height=30,
            command=lambda x: self.apply_filters()
        )
        self.category_filter.set("All")
        self.category_filter.place(x=300, y=150)
        
        # Clear filters button
        ctk.CTkButton(
            self,
            text="Clear Filters",
            width=100,
            height=30,
            fg_color="#6c757d",
            command=self.clear_filters
        ).place(x=1080, y=150)
    
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
        """Load and refresh items table data."""
        self.apply_filters()
        self._update_category_filter()
    
    def _update_category_filter(self) -> None:
        """Update category filter dropdown with available categories."""
        try:
            from database.queries import get_all_categories
            categories = get_all_categories()
            self.category_filter.configure(values=["All"] + categories)
        except Exception as e:
            print(f"Error loading categories: {e}")
    
    def apply_filters(self) -> None:
        """Apply search and filter criteria to the table."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.item_map = {}  # Reset map
        
        try:
            from database.queries import search_items
            
            # Get filter values
            search_term = self.search_entry.get().strip()
            status_val = self.status_filter.get()
            type_val = self.type_filter.get()
            category_val = self.category_filter.get()
            
            # Convert "All" to None for query
            status_filter = None if status_val == "All" else status_val
            type_filter = None if type_val == "All" else type_val
            category_filter = None if category_val == "All" else category_val
            
            # Search items
            items = search_items(
                search_term=search_term,
                status_filter=status_filter,
                type_filter=type_filter,
                category_filter=category_filter
            )
            
            for index, item in enumerate(items):
                # item structure: (id, name, landmark, date, time, username, type, desc, image, status, category)
                row_values = (
                    item[1],  # name
                    item[2],  # landmark
                    item[3],  # date
                    item[4],  # time
                    item[5],  # username
                    item[9] if len(item) > 9 else "Unknown",  # status
                    item[10] if len(item) > 10 else "Uncategorized"  # category
                )
                
                self.tree.insert("", "end", iid=index, values=row_values)
                self.item_map[index] = item
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load items: {str(e)}")
    
    def clear_filters(self) -> None:
        """Clear all search and filter inputs."""
        self.search_entry.delete(0, 'end')
        self.status_filter.set("All")
        self.type_filter.set("All")
        self.category_filter.set("All")
        self.apply_filters()
    
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

