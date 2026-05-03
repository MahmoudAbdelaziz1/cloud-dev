from tkinter import *
from tkinter import messagebox
from cars_import import cars_import
from ui_theme import page, card, label, entry, action_button, back_button, get_connection, ensure_tables, CARD, NAVY_2, FONT, BORDER


def insert_data(root, clear_page, main_menu):
    clear_page(root)
    ensure_tables()

    def save_data():
        car_supplier_value = car_supplier.get()
        car_name_value = car_name.get()
        car_model_value = car_model.get()

        if not car_supplier_value or not car_name_value or not car_model_value:
            messagebox.showwarning("Error", "Please fill in all fields.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cars_info (car_type, car_model, car_supplier)
            VALUES(:car_type, :car_model, :car_supplier)
        """, {
            "car_type": car_name_value,
            "car_model": car_model_value,
            "car_supplier": car_supplier_value
        })
        conn.commit()
        conn.close()

        clear_page(root)
        cars_import(root, clear_page, main_menu, car_supplier_value, car_name_value, car_model_value)

    body = page(root, "Insert", "Create a basic car record before completing import details")

    form_card = card(body)
    form_card.pack(fill="x", padx=4, pady=4)
    for col in (1, 3):
        form_card.grid_columnconfigure(col, weight=1)

    Label(form_card, text="New Car Record", bg=CARD, fg=NAVY_2, font=(FONT, 18, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=24, pady=(22, 8))
    Frame(form_card, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4, sticky="ew", padx=24, pady=(0, 12))

    car_name = entry(form_card, width=26)
    label(form_card, "Car Name").grid(row=2, column=0, sticky="w", padx=(24, 12), pady=12)
    car_name.grid(row=2, column=1, sticky="ew", padx=(0, 24), pady=12, ipady=5)

    car_model = entry(form_card, width=26)
    label(form_card, "Car Model").grid(row=2, column=2, sticky="w", padx=(24, 12), pady=12)
    car_model.grid(row=2, column=3, sticky="ew", padx=(0, 24), pady=12, ipady=5)

    car_supplier = entry(form_card, width=26)
    label(form_card, "Car Supplier").grid(row=3, column=0, sticky="w", padx=(24, 12), pady=12)
    car_supplier.grid(row=3, column=1, sticky="ew", padx=(0, 24), pady=12, ipady=5)

    buttons = Frame(form_card, bg=CARD)
    buttons.grid(row=4, column=0, columnspan=4, sticky="e", padx=24, pady=(20, 22))
    back_button(buttons, lambda: main_menu(root, clear_page)).pack(side="left", padx=(0, 10))
    action_button(buttons, "Continue To Import", save_data, variant="primary", width=20).pack(side="left")
