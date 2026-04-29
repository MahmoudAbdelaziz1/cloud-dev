from pathlib import Path
from sqlite3 import connect
from tkinter import *
from tkinter import ttk
import sys

PROJECT_DIR = Path(__file__).resolve().parent

APP_TITLE = "AutoFlow Stock & Rental Management"
BRAND_NAME = "AutoFlow"
BRAND_SUBTITLE = "Stock & Rental"

# Clean executive dashboard palette
BG = "#EAF0F8"
BG_SOFT = "#F6F8FC"
NAVY = "#061426"
NAVY_2 = "#0B2342"
NAVY_3 = "#14365F"
ACCENT = "#D6A33B"
ACCENT_DARK = "#8D611C"
ACCENT_LIGHT = "#FFF1CF"
CARD = "#FFFFFF"
TEXT = "#111827"
MUTED = "#64748B"
BORDER = "#D8E4F2"
BORDER_DARK = "#263E5F"
SUCCESS = "#15845B"
DANGER = "#B42318"
INFO = "#2563EB"
TABLE_ALT = "#F8FBFF"

FONT = "Segoe UI"
TITLE_FONT = (FONT, 24, "bold")
SUBTITLE_FONT = (FONT, 10)
SECTION_FONT = (FONT, 15, "bold")
LABEL_FONT = (FONT, 10, "bold")
BODY_FONT = (FONT, 10)
BUTTON_FONT = (FONT, 10, "bold")
SMALL_FONT = (FONT, 9)


def resource_path(filename):
    return str(PROJECT_DIR / filename)


def database_path():
    return str(PROJECT_DIR / "cars.db")


def get_connection():
    return connect(database_path())


def ensure_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cars_info(
            car_type TEXT,
            car_model TEXT,
            car_price INTEGER,
            car_supplier TEXT,
            num INTEGER,
            color TEXT,
            price_buying INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rental_cars(
            car_type TEXT,
            car_model TEXT,
            car_price INTEGER,
            car_supplier TEXT,
            num INTEGER,
            color TEXT,
            price_buying INTEGER,
            client_name TEXT
        )
    """)
    conn.commit()
    conn.close()


def _set_windows_app_id():
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("autoflow.stock.rental.manager")
    except Exception:
        pass


def initialize_app_identity():
    _set_windows_app_id()


def apply_app_icon(window):
    _set_windows_app_id()
    try:
        window.iconbitmap(resource_path("app_logo.ico"))
    except Exception:
        pass
    for size in (96, 64, 32):
        try:
            icon = PhotoImage(file=resource_path(f"app_logo_{size}.png"))
            window._app_icon_image = icon
            window.iconphoto(True, icon)
            break
        except Exception:
            continue


def _center_window(root, width=1366, height=780):
    try:
        root.update_idletasks()
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        width = min(width, max(1120, screen_w - 70))
        height = min(height, max(700, screen_h - 90))
        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
    except Exception:
        root.geometry("1366x780")


def setup_window(root):
    root.title(APP_TITLE)
    root.minsize(1120, 680)
    root.configure(bg=BG)
    apply_app_icon(root)
    configure_styles()
    _center_window(root)


def configure_styles():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except TclError:
        pass

    style.configure(
        "Treeview",
        background=CARD,
        fieldbackground=CARD,
        foreground=TEXT,
        rowheight=33,
        borderwidth=0,
        font=(FONT, 10),
        relief="flat",
    )
    style.configure(
        "Treeview.Heading",
        background=NAVY_2,
        foreground="white",
        font=(FONT, 10, "bold"),
        padding=(10, 9),
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", "white")],
    )
    style.configure(
        "TCombobox",
        fieldbackground="white",
        background="white",
        foreground=TEXT,
        arrowcolor=NAVY,
        padding=(8, 7),
        font=BODY_FONT,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        relief="flat",
    )
    style.map("TCombobox", fieldbackground=[("readonly", "white")])
    style.configure("Vertical.TScrollbar", background=BG_SOFT, troughcolor=CARD, bordercolor=CARD, arrowcolor=NAVY_2)
    style.configure("Horizontal.TScrollbar", background=BG_SOFT, troughcolor=CARD, bordercolor=CARD, arrowcolor=NAVY_2)


def clear_root(root):
    try:
        root.unbind("<Return>")
    except Exception:
        pass
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg=BG)
    configure_styles()


def logo_label(parent, size=64, bg=None):
    background = bg if bg is not None else parent.cget("bg")
    try:
        image = PhotoImage(file=resource_path(f"app_logo_{size}.png"))
        root = parent.winfo_toplevel()
        if not hasattr(root, "_logo_refs"):
            root._logo_refs = []
        root._logo_refs.append(image)
        return Label(parent, image=image, bg=background, bd=0)
    except Exception:
        return Label(parent, text="AF", bg=background, fg=ACCENT, font=(FONT, 22, "bold"), bd=0)


def _divider(parent, bg=BORDER):
    return Frame(parent, bg=bg, height=1)


def _pill(parent, text, bg=ACCENT_LIGHT, fg=ACCENT_DARK):
    box = Frame(parent, bg=bg, highlightthickness=1, highlightbackground=bg)
    Label(box, text=text, bg=bg, fg=fg, font=(FONT, 8, "bold")).pack(padx=10, pady=5)
    return box


def _sidebar(parent, active_title):
    side = Frame(parent, bg=NAVY, width=238)
    side.pack(side="left", fill="y")
    side.pack_propagate(False)

    brand = Frame(side, bg=NAVY)
    brand.pack(fill="x", padx=18, pady=(20, 16))
    logo_label(brand, size=64, bg=NAVY).pack(side="left")

    title_box = Frame(brand, bg=NAVY)
    title_box.pack(side="left", padx=10, fill="x", expand=True)
    Label(title_box, text=BRAND_NAME, bg=NAVY, fg="white", font=(FONT, 17, "bold")).pack(anchor="w")
    Label(title_box, text=BRAND_SUBTITLE, bg=NAVY, fg="#A7B8CF", font=(FONT, 9, "bold")).pack(anchor="w")

    _divider(side, BORDER_DARK).pack(fill="x", padx=18, pady=(0, 16))

    Label(side, text="ACTIVE PAGE", bg=NAVY, fg="#74849A", font=(FONT, 8, "bold")).pack(anchor="w", padx=21, pady=(0, 7))
    active = Frame(side, bg=NAVY_2, highlightthickness=1, highlightbackground="#2B4569")
    active.pack(fill="x", padx=14, pady=(0, 18))
    Frame(active, bg=ACCENT, width=5).pack(side="left", fill="y")
    Label(active, text=active_title, bg=NAVY_2, fg="white", font=(FONT, 10, "bold"), anchor="w", wraplength=170, justify="left").pack(side="left", fill="x", expand=True, padx=11, pady=11)

    Label(side, text="WORKSPACE", bg=NAVY, fg="#74849A", font=(FONT, 8, "bold")).pack(anchor="w", padx=21, pady=(0, 7))
    modules = [
        ("01", "Stock Import"),
        ("02", "Sales"),
        ("03", "Rental Requests"),
        ("04", "Records"),
        ("05", "Returned Cars"),
        ("06", "Company Info"),
    ]
    for code, item in modules:
        row = Frame(side, bg=NAVY)
        row.pack(fill="x", padx=17, pady=3)
        Label(row, text=code, bg="#0D213B", fg=ACCENT, font=(FONT, 8, "bold"), width=4).pack(side="left", ipady=4)
        Label(row, text=item, bg=NAVY, fg="#D7E1EF", font=(FONT, 9), anchor="w").pack(side="left", padx=9)

    bottom = Frame(side, bg="#0D213B", highlightthickness=1, highlightbackground="#243B5A")
    bottom.pack(side="bottom", fill="x", padx=17, pady=18)
    Label(bottom, text="Car operations suite", bg="#0D213B", fg="white", font=(FONT, 9, "bold")).pack(anchor="w", padx=12, pady=(11, 2))
    Label(bottom, text="Stock • Sales • Rentals", bg="#0D213B", fg="#98A9C2", font=(FONT, 8)).pack(anchor="w", padx=12, pady=(0, 11))


def page(root, title, subtitle=""):
    root.configure(bg=BG)

    shell = Frame(root, bg=BG)
    shell.pack(fill="both", expand=True)

    _sidebar(shell, title)

    main = Frame(shell, bg=BG)
    main.pack(side="left", fill="both", expand=True)

    top = Frame(main, bg=BG)
    top.pack(fill="x", padx=22, pady=(18, 0))

    header_shadow = Frame(top, bg="#D5DFEC")
    header_shadow.pack(fill="x")

    header = Frame(header_shadow, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
    header.pack(fill="x", padx=(0, 2), pady=(0, 3))
    header.grid_columnconfigure(1, weight=1)

    Frame(header, bg=ACCENT, width=6).grid(row=0, column=0, sticky="ns")

    title_area = Frame(header, bg=CARD)
    title_area.grid(row=0, column=1, sticky="ew", padx=20, pady=13)
    Label(title_area, text=title, bg=CARD, fg=NAVY, font=TITLE_FONT, anchor="w").pack(anchor="w")
    if subtitle:
        Label(title_area, text=subtitle, bg=CARD, fg=MUTED, font=SUBTITLE_FONT, anchor="w", wraplength=760, justify="left").pack(anchor="w", pady=(2, 0))

    _pill(header, "READY").grid(row=0, column=2, sticky="e", padx=18, pady=17)

    body = Frame(main, bg=BG)
    body.pack(fill="both", expand=True, padx=22, pady=18)
    body.grid_columnconfigure(0, weight=1)
    body.grid_rowconfigure(0, weight=1)
    return body


def card(parent, **pack_options):
    frame = Frame(parent, bg=CARD, bd=0, highlightthickness=1, highlightbackground=BORDER)
    if pack_options:
        frame.pack(**pack_options)
    return frame


def section_title(parent, text):
    return Label(parent, text=text, bg=CARD, fg=NAVY, font=SECTION_FONT)


def section_header(parent, title, subtitle=None):
    container = Frame(parent, bg=CARD)
    Label(container, text=title, bg=CARD, fg=NAVY, font=SECTION_FONT).pack(anchor="w")
    if subtitle:
        Label(container, text=subtitle, bg=CARD, fg=MUTED, font=SMALL_FONT, wraplength=560, justify="left").pack(anchor="w", pady=(3, 0))
    return container


def label(parent, text, bg=CARD):
    return Label(parent, text=text, bg=bg, fg=TEXT, font=LABEL_FONT)


def muted(parent, text, bg=CARD):
    return Label(parent, text=text, bg=bg, fg=MUTED, font=BODY_FONT)


def entry(parent, width=28, show=None, textvariable=None, state=None):
    e = Entry(
        parent,
        width=width,
        show=show,
        textvariable=textvariable,
        state=state,
        bg="white",
        fg=TEXT,
        disabledbackground="#F4F7FB",
        readonlybackground="#F4F7FB",
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        insertbackground=TEXT,
        font=(FONT, 11),
        relief="flat",
    )
    e.bind("<FocusIn>", lambda _event: e.configure(highlightbackground=ACCENT))
    e.bind("<FocusOut>", lambda _event: e.configure(highlightbackground=BORDER))
    return e


def _button_colors(variant):
    colors = {
        "primary": (ACCENT, ACCENT_DARK, "white"),
        "secondary": (NAVY_2, NAVY, "white"),
        "success": (SUCCESS, "#0F6B4A", "white"),
        "danger": (DANGER, "#8F1D15", "white"),
        "info": (INFO, "#1D4ED8", "white"),
        "light": ("#F1F5FA", "#E3EBF6", NAVY_2),
    }
    return colors.get(variant, colors["primary"])


def action_button(parent, text, command, variant="primary", width=16):
    normal_bg, hover_bg, fg = _button_colors(variant)
    btn = Button(
        parent,
        text=text,
        command=command,
        width=width,
        height=1,
        bg=normal_bg,
        fg=fg,
        activebackground=hover_bg,
        activeforeground=fg,
        bd=0,
        relief="flat",
        cursor="hand2",
        font=BUTTON_FONT,
        padx=13,
        pady=8,
    )
    btn.bind("<Enter>", lambda _event: btn.configure(bg=hover_bg))
    btn.bind("<Leave>", lambda _event: btn.configure(bg=normal_bg))
    return btn


def back_button(parent, command):
    return action_button(parent, "Back", command, variant="light", width=12)


def form_row(parent, row, text, widget, label_col=0, field_col=1, padx=(24, 12), pady=10):
    label(parent, text).grid(row=row, column=label_col, sticky="w", padx=padx, pady=pady)
    widget.grid(row=row, column=field_col, sticky="ew", padx=(0, 24), pady=pady, ipady=5)


def table(parent, columns, rows, height=10, widths=None):
    wrapper = Frame(parent, bg=CARD)
    tree = ttk.Treeview(wrapper, columns=columns, show="headings", height=height)
    yscroll = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
    xscroll = ttk.Scrollbar(wrapper, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

    tree.tag_configure("odd", background=CARD)
    tree.tag_configure("even", background=TABLE_ALT)

    for col in columns:
        tree.heading(col, text=col)
        width = widths.get(col, 138) if widths else 138
        tree.column(col, width=width, anchor="center", stretch=True, minwidth=82)

    for index, row in enumerate(rows):
        tree.insert("", END, values=row, tags=("even" if index % 2 == 0 else "odd",))

    tree.grid(row=0, column=0, sticky="nsew")
    yscroll.grid(row=0, column=1, sticky="ns")
    xscroll.grid(row=1, column=0, sticky="ew")
    wrapper.grid_rowconfigure(0, weight=1)
    wrapper.grid_columnconfigure(0, weight=1)
    return wrapper, tree


def make_stat(parent, title, value, column):
    outer = Frame(parent, bg="#CBD8E8")
    outer.grid(row=0, column=column, sticky="ew", padx=7, pady=(0, 14))
    box = Frame(outer, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
    box.pack(fill="both", expand=True, padx=(0, 2), pady=(0, 3))

    top = Frame(box, bg=CARD)
    top.pack(fill="x", padx=15, pady=(13, 1))
    Frame(top, bg=ACCENT, width=5, height=21).pack(side="left")
    Label(top, text=title, bg=CARD, fg=MUTED, font=(FONT, 10, "bold")).pack(side="left", padx=9)

    Label(box, text=str(value), bg=CARD, fg=NAVY, font=(FONT, 23, "bold")).pack(anchor="w", padx=15, pady=(0, 13))
    return outer


def info_banner(parent, title, text):
    banner = Frame(parent, bg="#F8FAFC", highlightthickness=1, highlightbackground=BORDER)
    Label(banner, text=title, bg="#F8FAFC", fg=NAVY, font=(FONT, 11, "bold")).pack(anchor="w", padx=15, pady=(11, 2))
    Label(banner, text=text, bg="#F8FAFC", fg=MUTED, font=SMALL_FONT, justify="left", wraplength=650).pack(anchor="w", padx=15, pady=(0, 11))
    return banner


def menu_tile(parent, code, title, description, command):
    tile = card(parent)
    tile.grid_propagate(False)

    top = Frame(tile, bg=CARD)
    top.pack(fill="x", padx=18, pady=(18, 8))

    badge = Frame(top, bg=ACCENT_LIGHT, highlightthickness=1, highlightbackground="#E7C981", width=50, height=50)
    badge.pack(side="left")
    badge.pack_propagate(False)
    Label(badge, text=code, bg=ACCENT_LIGHT, fg=ACCENT_DARK, font=(FONT, 12, "bold")).pack(expand=True)

    Label(top, text=title, bg=CARD, fg=NAVY, font=(FONT, 15, "bold"), anchor="w", wraplength=240, justify="left").pack(side="left", padx=12, fill="x", expand=True)

    Label(tile, text=description, bg=CARD, fg=MUTED, font=(FONT, 10), wraplength=285, justify="left", anchor="w").pack(anchor="w", padx=18, pady=(0, 12))
    action_button(tile, "Open", command, variant="primary", width=12).pack(anchor="w", padx=18, pady=(0, 18))

    def enter(_event):
        tile.configure(highlightbackground=ACCENT)

    def leave(_event):
        tile.configure(highlightbackground=BORDER)

    for target in [tile] + tile.winfo_children():
        target.bind("<Enter>", enter)
        target.bind("<Leave>", leave)
    return tile
