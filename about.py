from tkinter import *
from tkinter import PhotoImage
import webbrowser
from ui_theme import page, card, section_title, muted, action_button, back_button, resource_path, logo_label, CARD, NAVY, TEXT, MUTED, BORDER, FONT, ACCENT, ACCENT_LIGHT, ACCENT_DARK


def about(root, clear_page, main_menu):
    clear_page(root)

    def open_link(url):
        webbrowser.open_new(url)

    def load_icon(filename):
        try:
            return PhotoImage(file=resource_path(filename))
        except Exception:
            return None

    root.fb_icon = load_icon("facebook.png")
    root.insta_icon = load_icon("instagram.png")
    root.yt_icon = load_icon("youtube.png")
    root.linkedin_icon = load_icon("linkedin.png")
    root.contact_icon = load_icon("contact.png")

    body = page(root, "Ghabbour Auto Group", "Company overview and official contact information")

    layout = Frame(body, bg=body["bg"])
    layout.pack(fill="both", expand=True)
    layout.grid_columnconfigure(0, weight=2)
    layout.grid_columnconfigure(1, weight=1)
    layout.grid_rowconfigure(0, weight=1)

    left_card = card(layout)
    left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    left_card.grid_columnconfigure(0, weight=1)

    hero = Frame(left_card, bg=CARD)
    hero.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
    logo_label(hero, size=64, bg=CARD).pack(side="left")
    title_box = Frame(hero, bg=CARD)
    title_box.pack(side="left", padx=14, fill="x", expand=True)
    Label(title_box, text="Company Profile", bg=CARD, fg=NAVY, font=(FONT, 20, "bold")).pack(anchor="w")
    Label(title_box, text="Automotive trading, distribution, and after-sales services", bg=CARD, fg=MUTED, font=(FONT, 10)).pack(anchor="w", pady=(2, 0))

    Frame(left_card, bg=BORDER, height=1).grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 14))

    section_title(left_card, "Overview").grid(row=2, column=0, sticky="w", padx=24, pady=(0, 8))
    Label(left_card, text=(
        "Ghabbour Auto Group is an automotive company specializing in trading, "
        "distributing, and marketing all types of transportation, including heavy trucks "
        "and semi-trucks."
    ), bg=CARD, fg=TEXT, font=(FONT, 12), justify="left", wraplength=680).grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 18))

    section_title(left_card, "Mission Statement").grid(row=4, column=0, sticky="w", padx=24, pady=(0, 8))
    Label(left_card, text=(
        "GB Auto is a leading automotive player in the Middle East, with a strong footprint "
        "in key sectors. Its primary lines of business are Passenger Cars, Motorcycles & "
        "Three-Wheelers, Commercial Vehicles & Construction Equipment, After-Sales, and Tires.\n\n"
        "In addition to providing after-sales services, the company operates several business "
        "lines across Egypt and Iraq."
    ), bg=CARD, fg=TEXT, font=(FONT, 12), justify="left", wraplength=680).grid(row=5, column=0, sticky="ew", padx=24, pady=(0, 18))

    muted(left_card, "© 2024 Ghabbour Auto Group - All Rights Reserved", bg=CARD).grid(row=6, column=0, sticky="w", padx=24, pady=(10, 22))

    right_card = card(layout)
    right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    Label(right_card, text="Contact Links", bg=CARD, fg=NAVY, font=(FONT, 18, "bold")).pack(anchor="w", padx=22, pady=(24, 6))
    Label(right_card, text="Open the official company channels.", bg=CARD, fg=MUTED, font=(FONT, 10), wraplength=250, justify="left").pack(anchor="w", padx=22, pady=(0, 14))
    Frame(right_card, bg=BORDER, height=1).pack(fill="x", padx=22, pady=(0, 12))

    links = [
        ("Facebook", root.fb_icon, "https://www.facebook.com/GBCorpMEA"),
        ("Instagram", root.insta_icon, "https://www.instagram.com/gbcorpmea/"),
        ("YouTube", root.yt_icon, "https://www.youtube.com/channel/UCx60Gg1pLM0WcZTInT2g6Ig"),
        ("LinkedIn", root.linkedin_icon, "https://www.linkedin.com/company/gbcorpmea/"),
        ("Contact Us", root.contact_icon, "https://gb-corporation.com/#!/contact-us"),
    ]

    for text, icon, url in links:
        row = Frame(right_card, bg="#F8FAFC", highlightthickness=1, highlightbackground=BORDER)
        row.pack(fill="x", padx=22, pady=6)
        Label(row, text=text, bg="#F8FAFC", fg=NAVY, font=(FONT, 10, "bold"), width=11, anchor="w").pack(side="left", padx=(12, 6), pady=9)
        if icon:
            Button(row, image=icon, command=lambda u=url: open_link(u), bd=0, bg="#F8FAFC", activebackground="#F8FAFC", cursor="hand2").pack(side="right", padx=10, pady=6)
        else:
            action_button(row, "Open", lambda u=url: open_link(u), variant="light", width=9).pack(side="right", padx=10, pady=6)

    bottom = Frame(right_card, bg=CARD)
    bottom.pack(side="bottom", fill="x", padx=22, pady=22)
    back_button(bottom, lambda: main_menu(root, clear_page)).pack(side="right")
