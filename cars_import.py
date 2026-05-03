from tkinter import *
from tkinter import ttk, messagebox
from ui_theme import page, card, label, entry, action_button, back_button, get_connection, ensure_tables, CARD, NAVY_2, FONT, BORDER, ACCENT, ACCENT_LIGHT, ACCENT_DARK


def cars_import(root, clear_page, main_menu, x=" ", y=" ", z=" "):
    clear_page(root)
    ensure_tables()

    def save_data():
        supplier = supplier_combobox.get()
        car_name = car_name_combobox.get()
        car_model = car_model_combobox.get()
        car_color = color_var.get()
        price = price_entry.get()
        pieces = pieces_entry.get()
        buying_price = buying_price_entry.get()

        if not supplier or not car_name or not car_model or not car_color or not price or not pieces or not buying_price:
            messagebox.showwarning("Error", "Please fill in the fields again and make sure they are correct.")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO cars_info (car_type, car_model, car_supplier, color, car_price, num, price_buying)
                VALUES (:car_name, :car_model, :supplier, :color, :price, :pieces, :buying_price)
            """, {
                "car_name": car_name,
                "car_model": car_model,
                "supplier": supplier,
                "color": car_color,
                "price": int(price),
                "pieces": int(pieces),
                "buying_price": int(buying_price)
            })
            cur.execute("DELETE FROM cars_info WHERE color IS NULL")
            conn.commit()
            messagebox.showinfo("Information", "Data saved successfully!")
            clear_page(root)
            main_menu(root, clear_page)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {e}")
        finally:
            try:
                conn.close()
            except Exception:
                pass

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT car_type FROM cars_info WHERE car_type IS NOT NULL")
    car_names = [car[0] for car in cur.fetchall()]
    cur.execute("SELECT DISTINCT car_model FROM cars_info WHERE car_model IS NOT NULL")
    car_models = [car[0] for car in cur.fetchall()]
    cur.execute("SELECT DISTINCT car_supplier FROM cars_info WHERE car_supplier IS NOT NULL")
    car_suppliers = [car[0] for car in cur.fetchall()]
    conn.close()

    body = page(root, "Car Import", "Add complete car information to the stock database")

    form_card = card(body)
    form_card.pack(fill="x", padx=4, pady=4)
    for col in (1, 3):
        form_card.grid_columnconfigure(col, weight=1)

    Label(form_card, text="Import Details", bg=CARD, fg=NAVY_2, font=(FONT, 18, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=24, pady=(22, 8))
    Frame(form_card, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4, sticky="ew", padx=24, pady=(0, 12))

    supplier_combobox = ttk.Combobox(form_card, state="readonly", font=(FONT, 11))
    supplier_combobox["values"] = car_suppliers
    supplier_combobox.set(x)
    label(form_card, "Supplier").grid(row=2, column=0, sticky="w", padx=(24, 12), pady=11)
    supplier_combobox.grid(row=2, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=4)

    car_name_combobox = ttk.Combobox(form_card, state="readonly", font=(FONT, 11))
    car_name_combobox["values"] = car_names
    car_name_combobox.set(y)
    label(form_card, "Car Name").grid(row=2, column=2, sticky="w", padx=(24, 12), pady=11)
    car_name_combobox.grid(row=2, column=3, sticky="ew", padx=(0, 24), pady=11, ipady=4)

    car_model_combobox = ttk.Combobox(form_card, state="readonly", font=(FONT, 11))
    car_model_combobox["values"] = car_models
    car_model_combobox.set(z)
    label(form_card, "Car Model").grid(row=3, column=0, sticky="w", padx=(24, 12), pady=11)
    car_model_combobox.grid(row=3, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=4)

    color_var = StringVar(value="Gray")
    label(form_card, "Car Color").grid(row=3, column=2, sticky="w", padx=(24, 12), pady=11)
    color_frame = Frame(form_card, bg=CARD)
    color_frame.grid(row=3, column=3, sticky="w", padx=(0, 24), pady=11)
    colors = [("Gray", "Gray"), ("Red", "Red"), ("Black", "Black"), ("Blue", "Blue")]
    for i, (color_name, value) in enumerate(colors):
        Radiobutton(color_frame, text=color_name, variable=color_var, value=value, bg=CARD,
                    fg=NAVY_2, selectcolor=ACCENT_LIGHT, activebackground=CARD,
                    activeforeground=ACCENT_DARK, font=(FONT, 10)).grid(row=0, column=i, padx=(0, 14))

    price_entry = entry(form_card, width=26)
    label(form_card, "Price of Car").grid(row=4, column=0, sticky="w", padx=(24, 12), pady=11)
    price_entry.grid(row=4, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    pieces_entry = entry(form_card, width=26)
    label(form_card, "Number of Pieces").grid(row=4, column=2, sticky="w", padx=(24, 12), pady=11)
    pieces_entry.grid(row=4, column=3, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    buying_price_entry = entry(form_card, width=26)
    label(form_card, "Buying Price").grid(row=5, column=0, sticky="w", padx=(24, 12), pady=11)
    buying_price_entry.grid(row=5, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    buttons = Frame(form_card, bg=CARD)
    buttons.grid(row=6, column=0, columnspan=4, sticky="e", padx=24, pady=(20, 22))
    back_button(buttons, lambda: main_menu(root, clear_page)).pack(side="left", padx=(0, 10))
    action_button(buttons, "Save", save_data, variant="primary", width=14).pack(side="left")
