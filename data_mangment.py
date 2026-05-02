from tkinter import *
from tkinter import messagebox
from insert_data import insert_data
from update_data import update_data
from ui_theme import page, card, action_button, back_button, table, get_connection, ensure_tables, CARD


def data_mangment(root, clear_page, main_menu):
    ensure_tables()
    clear_page(root)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT car_type, car_model, car_price, car_supplier, num, color, price_buying FROM cars_info")
    car_rows = cur.fetchall()
    conn.close()

    def get_selected_item():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a car record first.")
            return

        car_informations = tree.item(selected_item, "values")
        clear_page(root)
        update_data(root, clear_page, main_menu, data_mangment, car_informations)

    body = page(root, "Data Management", "View, insert, and update car stock records")

    table_card = card(body)
    table_card.pack(fill="both", expand=True)
    table_card.grid_rowconfigure(0, weight=1)
    table_card.grid_columnconfigure(0, weight=1)

    columns = ("Car Type", "Car Model", "Car Price", "Supplier", "Number", "Color", "Price Buying")
    widths = {"Car Type": 145, "Car Model": 145, "Car Price": 130, "Supplier": 170, "Number": 105, "Color": 110, "Price Buying": 140}
    table_frame, tree = table(table_card, columns, car_rows, height=13, widths=widths)
    table_frame.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

    actions = Frame(table_card, bg=CARD)
    actions.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 18))

    back_button(actions, lambda: main_menu(root, clear_page)).pack(side="right", padx=(10, 0))
    action_button(actions, "Insert", lambda: insert_data(root, clear_page, main_menu), variant="secondary", width=14).pack(side="right", padx=(10, 0))
    action_button(actions, "Update", get_selected_item, variant="primary", width=14).pack(side="right")
