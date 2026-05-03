from tkinter import *
from tkinter import messagebox
from ui_theme import page, card, label, entry, action_button, back_button, get_connection, CARD, NAVY_2, FONT, BORDER


def update_data(root, clear_page, main_menu, data_mangment, arr):
    clear_page(root)

    original_car_type = arr[0]
    original_car_model = arr[1]
    original_color = arr[5]

    def update_data_in_database():
        try:
            number_value = int(car_number.get())
            price_value = int(car_price.get())
            buying_value = int(car_Buying_price.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
            return

        conn = get_connection()
        cur = conn.cursor()

        if number_value == 0:
            cur.execute("""
                DELETE FROM cars_info
                WHERE car_type = :original_car_type
                AND car_model = :original_car_model
                AND color = :original_color
            """, {
                "original_car_type": original_car_type,
                "original_car_model": original_car_model,
                "original_color": original_color
            })
        else:
            cur.execute("""
                UPDATE cars_info
                SET car_type = :car_type,
                    car_model = :car_model,
                    car_supplier = :car_supplier,
                    car_price = :car_price,
                    color = :color,
                    price_buying = :price_buying,
                    num = :num
                WHERE car_type = :original_car_type
                AND car_model = :original_car_model
                AND color = :original_color
            """, {
                "car_type": car_name.get(),
                "car_model": car_model.get(),
                "car_supplier": car_supplier.get(),
                "car_price": price_value,
                "color": car_color.get(),
                "price_buying": buying_value,
                "num": number_value,
                "original_car_type": original_car_type,
                "original_car_model": original_car_model,
                "original_color": original_color
            })

        conn.commit()
        conn.close()
        clear_page(root)
        data_mangment(root, clear_page, main_menu)

    body = page(root, "Update", "Edit the selected car record")

    form_card = card(body)
    form_card.pack(fill="x", padx=4, pady=4)
    for col in (1, 3):
        form_card.grid_columnconfigure(col, weight=1)

    Label(form_card, text="Car Information", bg=CARD, fg=NAVY_2, font=(FONT, 18, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=24, pady=(22, 8))
    Frame(form_card, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4, sticky="ew", padx=24, pady=(0, 12))

    car_name = entry(form_card, width=24)
    car_name.insert(0, f"{arr[0]}")
    label(form_card, "Car Name").grid(row=2, column=0, sticky="w", padx=(24, 12), pady=11)
    car_name.grid(row=2, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    car_model = entry(form_card, width=24)
    car_model.insert(0, f"{arr[1]}")
    label(form_card, "Car Model").grid(row=2, column=2, sticky="w", padx=(24, 12), pady=11)
    car_model.grid(row=2, column=3, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    car_supplier = entry(form_card, width=24)
    car_supplier.insert(0, f"{arr[3]}")
    label(form_card, "Car Supplier").grid(row=3, column=0, sticky="w", padx=(24, 12), pady=11)
    car_supplier.grid(row=3, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    car_price = entry(form_card, width=24)
    car_price.insert(0, f"{arr[2]}")
    label(form_card, "Car Price").grid(row=3, column=2, sticky="w", padx=(24, 12), pady=11)
    car_price.grid(row=3, column=3, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    car_number = entry(form_card, width=24)
    car_number.insert(0, f"{arr[4]}")
    label(form_card, "Number of Pieces").grid(row=4, column=0, sticky="w", padx=(24, 12), pady=11)
    car_number.grid(row=4, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    car_color = entry(form_card, width=24)
    car_color.insert(0, f"{arr[5]}")
    label(form_card, "Car Color").grid(row=4, column=2, sticky="w", padx=(24, 12), pady=11)
    car_color.grid(row=4, column=3, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    car_Buying_price = entry(form_card, width=24)
    car_Buying_price.insert(0, f"{arr[6]}")
    label(form_card, "Buying Price").grid(row=5, column=0, sticky="w", padx=(24, 12), pady=11)
    car_Buying_price.grid(row=5, column=1, sticky="ew", padx=(0, 24), pady=11, ipady=5)

    buttons = Frame(form_card, bg=CARD)
    buttons.grid(row=6, column=0, columnspan=4, sticky="e", padx=24, pady=(20, 22))
    back_button(buttons, lambda: data_mangment(root, clear_page, main_menu)).pack(side="left", padx=(0, 10))
    action_button(buttons, "Save", update_data_in_database, variant="primary", width=14).pack(side="left")
