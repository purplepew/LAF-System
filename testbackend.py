from backend.lib.queries.users import get_all_users
from backend.lib.mutations.users import create_new_user
from backend.lib.utils import ensure_tables
from backend.lib.config import NAME_MIN_LENGTH, NAME_MAX_LENGTH, EMAIL_MIN_LENGTH, EMAIL_MAX_LENGTH
import tkinter as tk

print(get_all_users())