from tkinter import *
from tkinter import messagebox
from ui_theme import page, card, action_button, back_button, table, get_connection, ensure_tables, CARD


def rented_cars(root, clear_page, main_menu, data_mangment):
    clear_page(root)
    ensure_tables()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT car_type, car_model, car_price, car_supplier, num, color, price_buying, client_name FROM rental_cars")
    rental_rows = cur.fetchall()
    conn.close()

    def get_selected_item():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a rented car first.")
            return

        car_informations = tree.item(selected_item, "values")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT num FROM cars_info
            WHERE car_type = :car_type AND car_model = :car_model AND color = :color
        """, {
            "car_type": car_informations[0],
            "car_model": car_informations[1],
            "color": car_informations[5]
        })
        cars_select_info = cur.fetchone()

        if cars_select_info:
            cur.execute("""
                UPDATE cars_info
                SET car_type = :car_type,
                    car_model = :car_model,
                    car_price = :car_price,
                    car_supplier = :car_supplier,
                    num = num + 1,
                    color = :color,
                    price_buying = :price_buying
                WHERE car_type = :car_type AND car_model = :car_model AND color = :color
            """, {
                "car_type": car_informations[0],
                "car_model": car_informations[1],
                "car_price": car_informations[2],
                "car_supplier": car_informations[3],
                "color": car_informations[5],
                "price_buying": car_informations[6]
            })

            cur.execute("""
                DELETE FROM rental_cars
                WHERE car_type = :car_type
                AND car_model = :car_model
                AND color = :color
                AND client_name = :client_name
            """, {
                "car_type": car_informations[0],
                "car_model": car_informations[1],
                "color": car_informations[5],
                "client_name": car_informations[7]
            })
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Car received successfully.")
            clear_page(root)
            data_mangment(root, clear_page, main_menu)
        else:
            conn.close()
            messagebox.showwarning("Error", "This car record does not exist in stock.")

    body = page(root, "Car Rental", "Receive rented cars and return them to available stock")

    table_card = card(body)
    table_card.pack(fill="both", expand=True)
    table_card.grid_rowconfigure(0, weight=1)
    table_card.grid_columnconfigure(0, weight=1)

    columns = ("Car Type", "Car Model", "Car Price", "Supplier", "Number", "Color", "Price Buying", "Client Name")
    widths = {"Car Type": 130, "Car Model": 130, "Car Price": 122, "Supplier": 150, "Number": 95, "Color": 100, "Price Buying": 130, "Client Name": 160}
    table_frame, tree = table(table_card, columns, rental_rows, height=13, widths=widths)
    table_frame.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

    actions = Frame(table_card, bg=CARD)
    actions.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 18))
    back_button(actions, lambda: main_menu(root, clear_page)).pack(side="right", padx=(10, 0))
    action_button(actions, "Receive", get_selected_item, variant="primary", width=14).pack(side="right")
from tkinter import *
from tkinter import messagebox
from ui_theme import page, card, action_button, back_button, table, get_connection, ensure_tables, CARD


def rented_cars(root, clear_page, main_menu, data_mangment):
    clear_page(root)
    ensure_tables()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT car_type, car_model, car_price, car_supplier, num, color, price_buying, client_name FROM rental_cars")
    rental_rows = cur.fetchall()
    conn.close()

    def get_selected_item():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a rented car first.")
            return

        car_informations = tree.item(selected_item, "values")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT num FROM cars_info
            WHERE car_type = :car_type AND car_model = :car_model AND color = :color
        """, {
            "car_type": car_informations[0],
            "car_model": car_informations[1],
            "color": car_informations[5]
        })
        cars_select_info = cur.fetchone()

        if cars_select_info:
            cur.execute("""
                UPDATE cars_info
                SET car_type = :car_type,
                    car_model = :car_model,
                    car_price = :car_price,
                    car_supplier = :car_supplier,
                    num = num + 1,
                    color = :color,
                    price_buying = :price_buying
                WHERE car_type = :car_type AND car_model = :car_model AND color = :color
            """, {
                "car_type": car_informations[0],
                "car_model": car_informations[1],
                "car_price": car_informations[2],
                "car_supplier": car_informations[3],
                "color": car_informations[5],
                "price_buying": car_informations[6]
            })

            cur.execute("""
                DELETE FROM rental_cars
                WHERE car_type = :car_type
                AND car_model = :car_model
                AND color = :color
                AND client_name = :client_name
            """, {
                "car_type": car_informations[0],
                "car_model": car_informations[1],
                "color": car_informations[5],
                "client_name": car_informations[7]
            })
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Car received successfully.")
            clear_page(root)
            data_mangment(root, clear_page, main_menu)
        else:
            conn.close()
            messagebox.showwarning("Error", "This car record does not exist in stock.")

    body = page(root, "Car Rental", "Receive rented cars and return them to available stock")

    table_card = card(body)
    table_card.pack(fill="both", expand=True)
    table_card.grid_rowconfigure(0, weight=1)
    table_card.grid_columnconfigure(0, weight=1)

    columns = ("Car Type", "Car Model", "Car Price", "Supplier", "Number", "Color", "Price Buying", "Client Name")
    widths = {"Car Type": 130, "Car Model": 130, "Car Price": 122, "Supplier": 150, "Number": 95, "Color": 100, "Price Buying": 130, "Client Name": 160}
    table_frame, tree = table(table_card, columns, rental_rows, height=13, widths=widths)
    table_frame.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

    actions = Frame(table_card, bg=CARD)
    actions.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 18))
    back_button(actions, lambda: main_menu(root, clear_page)).pack(side="right", padx=(10, 0))
    action_button(actions, "Receive", get_selected_item, variant="primary", width=14).pack(side="right")
