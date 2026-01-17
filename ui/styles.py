"""
UI styles and reusable widget creation functions.
Centralizes fonts, colors, and common UI components to satisfy DRY principle.
"""
import customtkinter as ctk
from typing import Optional, Callable


# Color constants
PRIMARY_COLOR = "#2b9348"
SECONDARY_COLOR = "#495057"
ERROR_COLOR = "red"
SUCCESS_COLOR = "#2b9348"

# Card colors
CARD_YOUR_CLAIMED = "#ffadad"
CARD_TOTAL_CLAIMED = "#cdb4db"
CARD_PENDING = "#a2d2ff"
CARD_PROFILE = "#495057"
CARD_FORM = "#6c757d"

# Font families
FONT_FAMILY = "Poppins"


def create_header_label(
    parent: ctk.CTkFrame,
    text: str,
    font_size: int = 40,
    fg_color: str = "transparent"
) -> ctk.CTkLabel:
    """
    Create a standardized header label.
    
    Args:
        parent: Parent widget
        text: Label text
        font_size: Font size (default 40)
        fg_color: Foreground color
        
    Returns:
        CTkLabel widget
    """
    return ctk.CTkLabel(
        parent,
        font=(FONT_FAMILY, font_size, "bold"),
        text=text,
        fg_color=fg_color
    )


def create_title_label(
    parent: ctk.CTkFrame,
    text: str,
    font_size: int = 25,
    fg_color: str = "transparent"
) -> ctk.CTkLabel:
    """
    Create a standardized title label.
    
    Args:
        parent: Parent widget
        text: Label text
        font_size: Font size (default 25)
        fg_color: Foreground color
        
    Returns:
        CTkLabel widget
    """
    return ctk.CTkLabel(
        parent,
        font=(FONT_FAMILY, font_size, "bold"),
        text=text,
        fg_color=fg_color
    )


def create_entry(
    parent: ctk.CTkFrame,
    placeholder: str,
    width: int = 240,
    height: int = 40,
    show: Optional[str] = None
) -> ctk.CTkEntry:
    """
    Create a standardized entry widget.
    
    Args:
        parent: Parent widget
        placeholder: Placeholder text
        width: Entry width
        height: Entry height
        show: Character to show for password fields (e.g., "*")
        
    Returns:
        CTkEntry widget
    """
    return ctk.CTkEntry(
        parent,
        font=(FONT_FAMILY, 15),
        width=width,
        height=height,
        placeholder_text=placeholder,
        show=show
    )


def create_button(
    parent: ctk.CTkFrame,
    text: str,
    command: Optional[Callable] = None,
    width: int = 240,
    height: int = 40,
    fg_color: str = PRIMARY_COLOR,
    font_size: int = 15
) -> ctk.CTkButton:
    """
    Create a standardized button widget.
    
    Args:
        parent: Parent widget
        text: Button text
        command: Command function to execute on click
        width: Button width
        height: Button height
        fg_color: Button foreground color
        font_size: Font size
        
    Returns:
        CTkButton widget
    """
    return ctk.CTkButton(
        master=parent,
        font=(FONT_FAMILY, font_size, "bold" if font_size >= 15 else "normal"),
        fg_color=fg_color,
        width=width,
        height=height,
        hover=True,
        text=text,
        command=command
    )


def create_nav_button(
    parent: ctk.CTkFrame,
    text: str,
    command: Optional[Callable] = None,
    y_position: int = 0,
    height: int = 50
) -> ctk.CTkButton:
    """
    Create a standardized navigation menu button.
    
    Args:
        parent: Parent widget
        text: Button text
        command: Command function to execute on click
        y_position: Y position for placement
        height: Button height
        
    Returns:
        CTkButton widget
    """
    return ctk.CTkButton(
        parent,
        text=text,
        font=(FONT_FAMILY, 13 if text != "MENU" else 15, "bold"),
        height=height,
        width=200,
        fg_color=PRIMARY_COLOR,
        corner_radius=0,
        command=command
    )


def create_header_frame(
    parent: ctk.CTkFrame,
    title: str = "Lost and Found System"
) -> None:
    """
    Create the standard header frame and title.
    
    Args:
        parent: Parent widget
        title: Header title text
    """
    ctk.CTkFrame(
        parent,
        width=1000,
        height=70,
        fg_color=PRIMARY_COLOR,
        corner_radius=0
    ).place(x=201, y=0)
    
    ctk.CTkLabel(
        parent,
        font=(FONT_FAMILY, 20, "bold"),
        text=title,
        fg_color=PRIMARY_COLOR
    ).place(x=230, y=17)


def create_sidebar_frame(parent: ctk.CTkFrame) -> None:
    """
    Create the standard sidebar background frame.
    
    Args:
        parent: Parent widget
    """
    ctk.CTkFrame(
        parent,
        width=200,
        height=330,
        fg_color=PRIMARY_COLOR,
        corner_radius=0
    ).place(x=0, y=275)


def create_form_label(
    parent: ctk.CTkFrame,
    text: str,
    x: int,
    y: int,
    fg_color: str = CARD_FORM
) -> ctk.CTkLabel:
    """
    Create a form field label.
    
    Args:
        parent: Parent widget
        text: Label text
        x: X position
        y: Y position
        fg_color: Background color
        
    Returns:
        CTkLabel widget
    """
    return ctk.CTkLabel(
        parent,
        font=(FONT_FAMILY, 15, "bold"),
        text=text,
        fg_color=fg_color,
        text_color="White"
    )


def create_form_entry(
    parent: ctk.CTkFrame,
    placeholder: str,
    x: int,
    y: int,
    width: int = 460,
    height: int = 30
) -> ctk.CTkEntry:
    """
    Create a form entry field.
    
    Args:
        parent: Parent widget
        placeholder: Placeholder text
        x: X position
        y: Y position
        width: Entry width
        height: Entry height
        
    Returns:
        CTkEntry widget
    """
    return ctk.CTkEntry(
        parent,
        fg_color="#f8f9fa",
        width=width,
        height=height,
        text_color="black",
        placeholder_text=placeholder,
        corner_radius=7
    )

