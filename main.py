from tkinter import *
from main_menu import main_menu
from clear_page import clear_page
from password import password
from ui_theme import setup_window, ensure_tables, initialize_app_identity

initialize_app_identity()
root = Tk()
setup_window(root)
ensure_tables()

password(root, clear_page, main_menu)

root.mainloop()
