from backend.lib.queries.users import get_all_users
from backend.lib.mutations.items import create_new_item, seed_items
from backend.lib.utils import ensure_tables
from backend.lib.config import NAME_MIN_LENGTH, NAME_MAX_LENGTH, EMAIL_MIN_LENGTH, EMAIL_MAX_LENGTH
import tkinter as tk

ensure_tables()

# use only once to populate the items table
# seed_items() 
