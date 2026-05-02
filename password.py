from tkinter import *
from tkinter import messagebox
from ui_theme import (
    card, label, entry, action_button, muted, logo_label,
    APP_TITLE, BRAND_NAME, NAVY, NAVY_2, NAVY_3, ACCENT, CARD, MUTED, BG, BORDER, FONT
)


def password(root, clear_page, main_menu):
    clear_page(root)
    root.configure(bg=BG)

    shell = Frame(root, bg=BG)
    shell.pack(fill="both", expand=True)
    shell.grid_columnconfigure(0, weight=43)
    shell.grid_columnconfigure(1, weight=57)
    shell.grid_rowconfigure(0, weight=1)

    left = Frame(shell, bg=NAVY)
    left.grid(row=0, column=0, sticky="nsew")
    left.grid_columnconfigure(0, weight=1)
    left.grid_rowconfigure(3, weight=1)

    brand = Frame(left, bg=NAVY)
    brand.grid(row=0, column=0, sticky="nw", padx=48, pady=(46, 32))
    logo_label(brand, size=96, bg=NAVY).pack(side="left")
    brand_text = Frame(brand, bg=NAVY)
    brand_text.pack(side="left", padx=16)
    Label(brand_text, text=BRAND_NAME, bg=NAVY, fg="white", font=(FONT, 28, "bold")).pack(anchor="w")
    Label(brand_text, text="Stock & Rental Management", bg=NAVY, fg="#B7C7DD", font=(FONT, 11, "bold")).pack(anchor="w")

    Label(left, text=APP_TITLE, bg=NAVY, fg="white", font=(FONT, 28, "bold"), wraplength=420, justify="left").grid(row=1, column=0, sticky="nw", padx=52)
    Label(left, text="A simple desktop system for car stock, sales operations, rental requests, and returned vehicles.", bg=NAVY, fg="#C4D2E7", font=(FONT, 12), wraplength=430, justify="left").grid(row=2, column=0, sticky="nw", padx=52, pady=(16, 28))

    feature_box = Frame(left, bg=NAVY)
    feature_box.grid(row=3, column=0, sticky="nw", padx=54)
    features = [
        "Stock import and supplier records",
        "Sales quantity updates",
        "Rental request tracking",
        "Returned car receiving"
    ]
    for item in features:
        row = Frame(feature_box, bg=NAVY)
        row.pack(anchor="w", pady=6)
        Frame(row, bg=ACCENT, width=8, height=8).pack(side="left", pady=7)
        Label(row, text=item, bg=NAVY, fg="#E5ECF7", font=(FONT, 10, "bold")).pack(side="left", padx=11)

    footer = Frame(left, bg=NAVY_2, highlightthickness=1, highlightbackground="#2B4568")
    footer.grid(row=4, column=0, sticky="ew", padx=46, pady=(20, 36))
    Label(footer, text="Project workspace", bg=NAVY_2, fg="white", font=(FONT, 10, "bold")).pack(anchor="w", padx=16, pady=(13, 2))
    Label(footer, text="Data is saved locally inside the project folder", bg=NAVY_2, fg="#AFC0D6", font=(FONT, 9)).pack(anchor="w", padx=16, pady=(0, 13))

    right = Frame(shell, bg=BG)
    right.grid(row=0, column=1, sticky="nsew")
    right.grid_rowconfigure(0, weight=1)
    right.grid_columnconfigure(0, weight=1)

    login_card = card(right)
    login_card.grid(row=0, column=0, sticky="n", padx=68, pady=76, ipadx=6, ipady=6)
    login_card.grid_columnconfigure(0, weight=1)

    Frame(login_card, bg=ACCENT, height=5).grid(row=0, column=0, sticky="ew")

    Label(login_card, text="Welcome back", bg=CARD, fg=NAVY, font=(FONT, 27, "bold")).grid(row=1, column=0, sticky="w", padx=46, pady=(42, 6))
    muted(login_card, "Sign in to open the dashboard", bg=CARD).grid(row=2, column=0, sticky="w", padx=48, pady=(0, 28))

    form = Frame(login_card, bg=CARD)
    form.grid(row=3, column=0, sticky="ew", padx=46, pady=(0, 8))
    form.grid_columnconfigure(0, weight=1)

    label(form, "User name").grid(row=0, column=0, sticky="w", pady=(0, 7))
    username = entry(form, width=34)
    username.grid(row=1, column=0, sticky="ew", pady=(0, 18), ipady=6)

    label(form, "Password").grid(row=2, column=0, sticky="w", pady=(0, 7))
    password_key = entry(form, width=34, show="*")
    password_key.grid(row=3, column=0, sticky="ew", pady=(0, 24), ipady=6)

    def password_confirmation():
        if username.get() == "user" and password_key.get() == "12345":
            clear_page(root)
            main_menu(root, clear_page)
        else:
            messagebox.showerror("Login Error", "Incorrect username or password.")

    go = action_button(form, "Open Dashboard", password_confirmation, variant="primary", width=34)
    go.grid(row=4, column=0, sticky="ew")

    hint = Frame(login_card, bg="#F7FAFE", highlightthickness=1, highlightbackground=BORDER)
    hint.grid(row=4, column=0, sticky="ew", padx=46, pady=(22, 42))
    Label(hint, text="Account", bg="#F7FAFE", fg=NAVY_3, font=(FONT, 9, "bold")).pack(anchor="w", padx=14, pady=(10, 1))
    Label(hint, text="user / 12345", bg="#F7FAFE", fg=MUTED, font=(FONT, 9)).pack(anchor="w", padx=14, pady=(0, 10))

    username.focus_set()
    root.bind("<Return>", lambda event: password_confirmation())
