from tkinter import *
from tkinter import messagebox
from ui_theme import page, card, label, entry, action_button, back_button, table, get_connection, ensure_tables, apply_app_icon, CARD, BG, NAVY_2, BORDER, FONT


def create_Rent_Request(root, clear_page, main_menu):
    clear_page(root)
    ensure_tables()

    def choose_car():
        def get_selected_item():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Selection Required", "Please select a car first.")
                return

            car_details = tree.item(selected_item, "values")
            chosen_car_name.set(car_details[0])
            chosen_car_model.set(car_details[1])
            color.set(car_details[5])
            num.set(int(car_details[4]))
            car_window.destroy()

        car_window = Toplevel(root)
        car_window.title("Choose a Car")
        car_window.geometry("990x520")
        car_window.minsize(850, 460)
        car_window.configure(bg=BG)
        apply_app_icon(car_window)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT car_type, car_model, car_price, car_supplier, num, color, price_buying FROM cars_info")
        car_rows = cur.fetchall()
        conn.close()

        header = Frame(car_window, bg=NAVY_2, height=74)
        header.pack(fill="x")
        header.pack_propagate(False)
        Label(header, text="Choose a Car", bg=NAVY_2, fg="white", font=(FONT, 20, "bold")).pack(anchor="w", padx=24, pady=(15, 2))
        Label(header, text="Select a stock item to complete the rental request", bg=NAVY_2, fg="#A9BAD2", font=(FONT, 9)).pack(anchor="w", padx=25)

        table_card = card(car_window)
        table_card.pack(fill="both", expand=True, padx=22, pady=22)

        columns = ("Car Type", "Car Model", "Car Price", "Supplier", "Number", "Color", "Price Buying")
        table_frame, tree = table(table_card, columns, car_rows, height=9)
        table_frame.pack(fill="both", expand=True, padx=16, pady=(16, 10))

        action_button(table_card, "Select", get_selected_item, variant="primary", width=14).pack(anchor="e", padx=16, pady=(0, 16))

    def process_data():
        client_name = client_name_entry.get().strip()
        num_days = num_days_entry.get().strip()
        car_name = chosen_car_name.get().strip()
        car_model = chosen_car_model.get().strip()
        daily_price = Daily_Price.get().strip()

        if not client_name or not num_days or not car_name or not daily_price or not car_model:
            messagebox.showwarning("Missing Data", "Please fill all the fields!")
            return

        try:
            num_days_int = int(num_days)
            daily_price_float = float(daily_price)
            total_price = num_days_int * daily_price_float

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE cars_info
                SET num = :num
                WHERE car_type = :car_type AND car_model = :car_model AND color = :color
            """, {
                "car_type": car_name,
                "car_model": car_model,
                "color": color.get(),
                "num": max(0, num.get() - 1)
            })
            cur.execute("""
                INSERT INTO rental_cars (car_type, car_model, car_price, car_supplier, num, color, price_buying, client_name)
                SELECT car_type, car_model, car_price, car_supplier, :num, color, price_buying, :client_name
                FROM cars_info
                WHERE car_type = :car_type AND car_model = :car_model AND color = :color
            """, {
                "car_type": car_name,
                "car_model": car_model,
                "color": color.get(),
                "num": 1,
                "client_name": client_name
            })
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Car Rental",
                f"Rental Saved!\n\nClient: {client_name}\nCar: {car_name}\nTotal Price: ${total_price:.2f}"
            )
            clear_page(root)
            main_menu(root, clear_page)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for days and price.")

    chosen_car_name = StringVar()
    chosen_car_model = StringVar()
    color = StringVar()
    num = IntVar()

    body = page(root, "Car Rental Request", "Create and save a rental request")

    form_card = card(body)
    form_card.pack(fill="x", padx=4, pady=4)
    for col in (1, 3):
        form_card.grid_columnconfigure(col, weight=1)

    Label(form_card, text="Client & Car Details", bg=CARD, fg=NAVY_2, font=(FONT, 18, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=24, pady=(22, 8))
    Frame(form_card, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4, sticky="ew", padx=24, pady=(0, 12))

    client_name_entry = entry(form_card, width=26)
    label(form_card, "Client Name").grid(row=2, column=0, sticky="w", padx=(24, 12), pady=11)
    client_name_entry.grid(row=2, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    action_button(form_card, "Select Car", choose_car, variant="secondary", width=14).grid(row=2, column=3, sticky="e", padx=(0, 24), pady=11)

    car_name_entry = entry(form_card, width=26, textvariable=chosen_car_name, state="readonly")
    label(form_card, "Car Name").grid(row=3, column=0, sticky="w", padx=(24, 12), pady=11)
    car_name_entry.grid(row=3, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    car_model_entry = entry(form_card, width=18, textvariable=chosen_car_model, state="readonly")
    label(form_card, "Model").grid(row=3, column=2, sticky="w", padx=(24, 12), pady=11)
    car_model_entry.grid(row=3, column=3, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    num_days_entry = entry(form_card, width=26)
    label(form_card, "Number of Days").grid(row=4, column=0, sticky="w", padx=(24, 12), pady=11)
    num_days_entry.grid(row=4, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    Daily_Price = entry(form_card, width=26)
    label(form_card, "Daily Price").grid(row=4, column=2, sticky="w", padx=(24, 12), pady=11)
    Daily_Price.grid(row=4, column=3, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    buttons = Frame(form_card, bg=CARD)
    buttons.grid(row=5, column=0, columnspan=4, sticky="e", padx=24, pady=(20, 22))
    back_button(buttons, lambda: main_menu(root, clear_page)).pack(side="left", padx=(0, 10))
    action_button(buttons, "Save", process_data, variant="primary", width=14).pack(side="left")
