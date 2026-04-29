from tkinter import *
from tkinter import messagebox
from ui_theme import page, card, label, entry, action_button, back_button, table, get_connection, ensure_tables, CARD, NAVY_2, FONT, BORDER


def buyying(root, clear_page, main_menu):
    clear_page(root)
    ensure_tables()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT car_type, car_model, car_price, car_supplier, num, color, price_buying FROM cars_info")
    car_rows = cur.fetchall()
    conn.close()

    def choose_car():
        if table_card.winfo_ismapped():
            table_card.pack_forget()
        else:
            table_card.pack(fill="both", expand=True, pady=(16, 0))

    def submit():
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning("Error", "Please choose a car first.")
            return

        car_informations = tree.item(selected_item, "values")
        client_name = client_name_entry.get().strip()
        num_pieces = num_pieces_entry.get().strip()

        if not client_name or not num_pieces.isdigit():
            messagebox.showwarning("Error", "Please fill in all fields and make sure 'Number of Pieces' is a number.")
            return

        if int(num_pieces) > int(car_informations[4]):
            messagebox.showwarning("Error", "The number of pieces you entered is greater than what is in stock")
            clear_page(root)
            main_menu(root, clear_page)
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE cars_info
            SET num = :num
            WHERE car_type = :car_type AND car_model = :car_model AND color = :color
        """, {
            "car_type": car_informations[0],
            "car_model": car_informations[1],
            "color": car_informations[5],
            "num": int(car_informations[4]) - int(num_pieces)
        })
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Client Name: {client_name}\nNumber of Pieces: {num_pieces}")
        clear_page(root)
        main_menu(root, clear_page)

    body = page(root, "Buying", "Record customer purchases and update stock quantity")

    form_card = card(body)
    form_card.pack(fill="x")
    for col in (1, 3):
        form_card.grid_columnconfigure(col, weight=1)

    Label(form_card, text="Purchase Details", bg=CARD, fg=NAVY_2, font=(FONT, 18, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=24, pady=(22, 8))
    Frame(form_card, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4, sticky="ew", padx=24, pady=(0, 10))

    client_name_entry = entry(form_card, width=26)
    label(form_card, "Client Name").grid(row=2, column=0, sticky="w", padx=(24, 12), pady=12)
    client_name_entry.grid(row=2, column=1, sticky="ew", padx=(0, 24), pady=12, ipady=5)

    num_pieces_entry = entry(form_card, width=14)
    num_pieces_entry.insert(0, "0")
    label(form_card, "Number of Pieces").grid(row=2, column=2, sticky="w", padx=(24, 12), pady=12)
    num_pieces_entry.grid(row=2, column=3, sticky="ew", padx=(0, 24), pady=12, ipady=5)

    buttons = Frame(form_card, bg=CARD)
    buttons.grid(row=3, column=0, columnspan=4, sticky="e", padx=24, pady=(8, 22))
    back_button(buttons, lambda: main_menu(root, clear_page)).pack(side="left", padx=(0, 10))
    action_button(buttons, "Choose Car", choose_car, variant="secondary", width=14).pack(side="left", padx=(0, 10))
    action_button(buttons, "Save", submit, variant="primary", width=14).pack(side="left")

    table_card = card(body)
    columns = ("Car Type", "Car Model", "Car Price", "Supplier", "Number", "Color", "Price Buying")
    widths = {"Car Type": 145, "Car Model": 145, "Car Price": 130, "Supplier": 170, "Number": 105, "Color": 110, "Price Buying": 140}
    table_frame, tree = table(table_card, columns, car_rows, height=8, widths=widths)
    table_frame.pack(fill="both", expand=True, padx=18, pady=18)
