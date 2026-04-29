from tkinter import *
from cars_import import cars_import
from buyying import buyying
from password import password
from data_mangment import data_mangment
from create_Rent_Request import create_Rent_Request
from rented_cars import rented_cars
from about import about
from ui_theme import page, make_stat, menu_tile, back_button, get_connection, ensure_tables


def _counts():
    ensure_tables()
    conn = get_connection()
    cur = conn.cursor()
    try:
        total_cars = cur.execute("SELECT COALESCE(SUM(num), 0) FROM cars_info").fetchone()[0]
        types = cur.execute("SELECT COUNT(*) FROM cars_info").fetchone()[0]
        rented = cur.execute("SELECT COUNT(*) FROM rental_cars").fetchone()[0]
    finally:
        conn.close()
    return total_cars, types, rented


def main_menu(root, clear_page):
    clear_page(root)
    total_cars, types, rented = _counts()

    body = page(root, "Main Menu", "Choose a module and manage the car business workflow")

    stats = Frame(body, bg=body["bg"])
    stats.pack(fill="x", pady=(0, 14))
    for i, (title, value) in enumerate([
        ("Cars in Stock", total_cars),
        ("Stored Records", types),
        ("Rented Cars", rented),
    ]):
        make_stat(stats, title, value, i)
        stats.grid_columnconfigure(i, weight=1)

    grid = Frame(body, bg=body["bg"])
    grid.pack(fill="both", expand=True)

    items = [
        ("IM", "Car Import", "Add stock with supplier, model, color, quantity, and prices.", lambda: cars_import(root, clear_page, main_menu, " ", " ", " ")),
        ("BY", "Buying", "Record sold pieces and update available stock.", lambda: buyying(root, clear_page, main_menu)),
        ("RT", "Car Rental", "Create a new rental request for a selected car.", lambda: create_Rent_Request(root, clear_page, main_menu)),
        ("DM", "Data Management", "View all stock records and edit selected cars.", lambda: data_mangment(root, clear_page, main_menu)),
        ("RC", "Receiving Cars", "Receive returned rental cars and return them to stock.", lambda: rented_cars(root, clear_page, main_menu, data_mangment)),
        ("IN", "About", "Company overview and official contact links.", lambda: about(root, clear_page, main_menu)),
    ]

    for i, (code, title, desc, command) in enumerate(items):
        r, c = divmod(i, 3)
        tile = menu_tile(grid, code, title, desc, command)
        tile.grid(row=r, column=c, padx=9, pady=9, sticky="nsew")

    for c in range(3):
        grid.grid_columnconfigure(c, weight=1, uniform="menu")
    for r in range(2):
        grid.grid_rowconfigure(r, weight=1, uniform="menu")

    footer = Frame(body, bg=body["bg"])
    footer.pack(fill="x", pady=(6, 0))
    back_button(footer, lambda: password(root, clear_page, main_menu)).pack(side="right")
