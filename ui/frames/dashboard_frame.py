"""
Dashboard frame showing statistics and recent items.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from ui.styles import (
    create_header_frame, create_sidebar_frame, create_nav_button,
    CARD_YOUR_CLAIMED, CARD_TOTAL_CLAIMED, CARD_PENDING
)

if TYPE_CHECKING:
    from ui.app import App


class DashboardFrame(ctk.CTkFrame):
    """Frame displaying dashboard statistics and item table."""
    
    def __init__(self, parent: "App"):
        """
        Initialize the dashboard frame.
        
        Args:
            parent: The main App instance
        """
        super().__init__(parent)
        self.parent = parent
        self.place(relwidth=1, relheight=1)
        
        # Header and sidebar
        create_header_frame(self)
        create_sidebar_frame(self)
        
        # Title
        ctk.CTkLabel(
            self,
            font=("Poppins", 15, "bold"),
            text="Dashboard",
            fg_color="transparent"
        ).place(x=220, y=85)
        
        # Statistics cards
        self._create_stats_cards()
        
        # Table
        self._create_table()
        
        # Navigation buttons
        self._create_nav_buttons()
    
    def _create_stats_cards(self) -> None:
        """Create the statistics display cards."""
        # Your Claimed Items card
        ctk.CTkFrame(
            self,
            width=240,
            height=150,
            fg_color=CARD_YOUR_CLAIMED
        ).place(x=220, y=130)
        
        self.your_claimed_label = ctk.CTkLabel(
            self,
            font=("Poppins", 30, "bold"),
            text="0",
            fg_color=CARD_YOUR_CLAIMED
        )
        self.your_claimed_label.place(x=235, y=135)
        
        ctk.CTkLabel(
            self,
            font=("Poppins", 13, "bold"),
            text="Your Items",
            fg_color=CARD_YOUR_CLAIMED
        ).place(x=235, y=175)
        
        # Total Items card
        ctk.CTkFrame(
            self,
            width=240,
            height=150,
            fg_color=CARD_TOTAL_CLAIMED
        ).place(x=480, y=130)
        
        self.total_items_label = ctk.CTkLabel(
            self,
            font=("Poppins", 30, "bold"),
            text="0",
            fg_color=CARD_TOTAL_CLAIMED
        )
        self.total_items_label.place(x=495, y=135)
        
        ctk.CTkLabel(
            self,
            font=("Poppins", 13, "bold"),
            text="Total Items",
            fg_color=CARD_TOTAL_CLAIMED
        ).place(x=495, y=175)
        
        # Pending card
        ctk.CTkFrame(
            self,
            width=240,
            height=150,
            fg_color=CARD_PENDING
        ).place(x=740, y=130)
        
        self.pending_label = ctk.CTkLabel(
            self,
            font=("Poppins", 30, "bold"),
            text="0",
            fg_color=CARD_PENDING
        )
        self.pending_label.place(x=755, y=135)
        
        ctk.CTkLabel(
            self,
            font=("Poppins", 13, "bold"),
            text="Pending",
            fg_color=CARD_PENDING
        ).place(x=755, y=175)
    
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
        
        columns = ("Item Name", "Landmark", "Date Found", "Time Found", "Status")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=12
        )
        self.tree.place(x=210, y=300)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=155)
        
        scroll_y = tk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        scroll_y.place(x=1175, y=300, height=265)
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
            "My Items",
            command=lambda: self.parent.show_frame(self.parent.my_items_frame)
        ).place(x=0, y=224)
        
        create_nav_button(
            self,
            "Report Missing Items",
            command=lambda: self.parent.show_frame(self.parent.report_item_frame)
        ).place(x=0, y=275)
    
    def load_data(self) -> None:
        """Load and refresh dashboard statistics and table data."""
        current_id = self.parent.current_user_id
        
        if not current_id:
            return
        
        # Update statistics
        try:
            from database.queries import get_dashboard_stats
            
            stats = get_dashboard_stats(current_id)
            # stats: (your_items, total_items, pending)
            self.your_claimed_label.configure(text=str(stats[0]))
            self.total_items_label.configure(text=str(stats[1]))
            self.pending_label.configure(text=str(stats[2]))
        except Exception as e:
            print(f"Error loading stats: {e}")
        
        # Update table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            from database.queries import get_all_items
            
            items = get_all_items()
            
            for item in items:
                # item structure: (id, name, landmark, date, time, username, type, desc, image, status)
                status = item[9] if len(item) > 9 else "Unknown"
                row_data = (item[1], item[2], item[3], item[4], status)
                self.tree.insert("", "end", values=row_data)
        except Exception as e:
            print(f"Error loading dashboard table: {e}")

