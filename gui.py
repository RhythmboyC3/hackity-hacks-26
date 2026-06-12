"""Simple Tkinter timetable editor with a built-in main menu.

This GUI version lives alongside the existing terminal UI. It reads and writes the same
CSV file, with a polished main menu screen that is ready for additional features.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

CSV_PATH = "timetabledata.csv"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ROW_COUNT = 5

# Dark Mode Color Palette
BG_DARK = "#0f172a"
BG_SECONDARY = "#1e293b"
CARD_DARK = "#1e293b"
BORDER_DARK = "#334155"
TEXT_PRIMARY = "#f1f5f9"
TEXT_SECONDARY = "#cbd5e1"
PRIMARY = "#3b82f6"
PRIMARY_HOVER = "#2563eb"
ACCENT = "#10b981"
BUTTONBG = "#606060"
DANGER = "#ef4444"


def load_data():
    """Load the timetable CSV into a DataFrame.

    If the file does not exist, create a blank timetable file first.
    """
    try:
        df = pd.read_csv(CSV_PATH, dtype=object).fillna("")
    except FileNotFoundError:
        df = pd.DataFrame({day: ["" for _ in range(ROW_COUNT)] for day in DAYS})
        df.to_csv(CSV_PATH, index=False)
    return df.astype(str)


def save_data(values):
    """Save the current cell values into the CSV file."""
    df = pd.DataFrame(values, columns=DAYS)
    df.to_csv(CSV_PATH, index=False)


class TimetableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timetable Editor")
        self.geometry("1000x600")
        self.configure(bg=BG_DARK)
        self.resizable(False, False)

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure(
            "Primary.TButton",
            background=BUTTONBG,
            foreground=TEXT_PRIMARY,
            borderwidth=0,
            focusthickness=0,
            padding=8,
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", BORDER_DARK), ("disabled", BG_SECONDARY)],
            foreground=[("disabled", TEXT_PRIMARY)],
        )
        self.style.configure(
            "Danger.TButton",
            background="#7f1d1d",
            foreground=TEXT_PRIMARY,
            borderwidth=0,
            focusthickness=0,
            padding=8,
        )
        self.style.map(
            "Danger.TButton",
            background=[("active", "#991b1b"), ("disabled", "#7f1d1d")],
            foreground=[("disabled", TEXT_PRIMARY)],
        )

        self.cells = []
        self.data_frame = load_data()

        self.container = tk.Frame(self, bg=BG_DARK)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._build_main_menu()
        self._build_editor_screen()
        self.show_frame("menu")

    def _build_main_menu(self):
        frame = tk.Frame(self.container, bg=BG_DARK)

        card = tk.Frame(frame, bg=CARD_DARK, bd=1, relief="solid", highlightbackground=BORDER_DARK, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=16, pady=16)

        title = tk.Label(card, text="Main Menu", font=("Segoe UI", 28, "bold"), bg=CARD_DARK, fg=TEXT_PRIMARY)
        title.pack(pady=(28, 12))

        subtitle = tk.Label(
            card,
            text="Launch the timetable editor or explore upcoming features.",
            font=("Segoe UI", 12),
            bg=CARD_DARK,
            fg=TEXT_SECONDARY,
            wraplength=600,
            justify="center",
        )
        subtitle.pack(pady=(0, 28))

        button_frame = tk.Frame(card, bg=CARD_DARK)
        button_frame.pack(pady=(0, 24))

        timetable_button = ttk.Button(
            button_frame,
            text="📅 Open Timetable Editor",
            width=28,
            command=lambda: self.show_frame("editor"),
            style="Primary.TButton",
        )
        timetable_button.pack(pady=8)

        other_button = ttk.Button(
            button_frame,
            text="⚙️  Other Features (coming soon)",
            width=28,
            command=self.on_other_feature,
            style="Primary.TButton",
        )
        other_button.pack(pady=8)

        quit_button = ttk.Button(
            button_frame,
            text="❌ Quit",
            width=28,
            command=self.destroy,
            style="Primary.TButton",
        )
        quit_button.pack(pady=(16, 0))

        self.frames["menu"] = frame

    def _build_editor_screen(self):
        frame = tk.Frame(self.container, bg=BG_DARK)

        header_frame = tk.Frame(frame, bg=BG_DARK)
        header_frame.pack(fill="x", pady=(0, 20))

        back_button = ttk.Button(
            header_frame,
            text="← Back to Menu",
            width=14,
            command=lambda: self.show_frame("menu"),
            style="Primary.TButton",
        )
        back_button.pack(side="left")

        title_label = tk.Label(
            header_frame,
            text="📋 Timetable Editor",
            font=("Segoe UI", 22, "bold"),
            bg=BG_DARK,
            fg=TEXT_PRIMARY,
        )
        title_label.pack(side="left", padx=16)

        info_label = tk.Label(
            frame,
            text="Edit the cells directly and save when ready.",
            font=("Segoe UI", 11),
            bg=BG_DARK,
            fg=TEXT_SECONDARY,
        )
        info_label.pack(pady=(0, 14))

        table_card = tk.Frame(frame, bg=CARD_DARK, bd=1, relief="solid", highlightbackground=BORDER_DARK, highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=4, pady=(0, 18))

        self._build_table(table_card)
        self._build_buttons(frame)

        self.frames["editor"] = frame

    def _build_table(self, parent):
        self.cells = []
        self.data_frame = load_data()

        # Single unified table frame for proper alignment
        table_frame = tk.Frame(parent, bg=CARD_DARK)
        table_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Configure column weights for even distribution
        for col in range(len(DAYS)):
            table_frame.grid_columnconfigure(col, weight=1)

        # Header row
        for col, day in enumerate(DAYS):
            label = tk.Label(
                table_frame,
                text=day,
                font=("Segoe UI", 11, "bold"),
                bg=BG_SECONDARY,
                fg=ACCENT,
                borderwidth=1,
                relief="solid",
                pady=8,
                highlightbackground=BORDER_DARK,
            )
            label.grid(row=0, column=col, padx=1, pady=1, sticky="nsew")

        # Table body with rows
        for row in range(len(self.data_frame)):
            row_vars = []
            for col, day in enumerate(DAYS):
                value = self.data_frame.at[row, day]
                string_var = tk.StringVar(value=value)
                
                entry = tk.Entry(
                    table_frame,
                    textvariable=string_var,
                    font=("Segoe UI", 11),
                    relief="solid",
                    bd=1,
                    bg=BG_SECONDARY,
                    fg=TEXT_PRIMARY,
                    insertbackground=TEXT_PRIMARY,
                    selectbackground=PRIMARY,
                    selectforeground=TEXT_PRIMARY,
                    highlightbackground=BORDER_DARK,
                )
                entry.grid(row=row + 1, column=col, padx=1, pady=1, sticky="nsew")
                row_vars.append(string_var)
            self.cells.append(row_vars)

    def _build_buttons(self, parent):
        button_frame = tk.Frame(parent, bg=BG_DARK)
        button_frame.pack(pady=(8, 0))

        save_button = ttk.Button(
            button_frame,
            text="💾 Save",
            width=14,
            command=self.on_save,
            style="Primary.TButton",
        )
        save_button.grid(row=0, column=0, padx=8, pady=8)

        clear_button = ttk.Button(
            button_frame,
            text="🗑️  Clear All",
            width=14,
            command=self.on_clear,
            style="Danger.TButton",
        )
        clear_button.grid(row=0, column=1, padx=8, pady=8)

        reload_button = ttk.Button(
            button_frame,
            text="🔄 Reload",
            width=14,
            command=self.on_reload,
            style="Primary.TButton",
        )
        reload_button.grid(row=0, column=2, padx=8, pady=8)

        close_button = ttk.Button(
            button_frame,
            text="✖️  Close",
            width=14,
            command=self.destroy,
            style="Primary.TButton",
        )
        close_button.grid(row=0, column=3, padx=8, pady=8)

    def show_frame(self, name):
        if name == "editor":
            self._refresh_table_values()
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def _refresh_table_values(self):
        self.data_frame = load_data()
        for row, row_vars in enumerate(self.cells):
            for col, cell_var in enumerate(row_vars):
                cell_var.set(self.data_frame.at[row, DAYS[col]])

    def on_save(self):
        values = [[cell.get().strip() for cell in row] for row in self.cells]
        save_data(values)
        messagebox.showinfo("Saved", "Timetable saved to timetabledata.csv")

    def on_clear(self):
        if not messagebox.askyesno("Clear All", "Really clear the whole timetable?"):
            return

        for row_vars in self.cells:
            for cell in row_vars:
                cell.set("")

        self.on_save()

    def on_reload(self):
        self._refresh_table_values()
        messagebox.showinfo("Reloaded", "Timetable reloaded from timetabledata.csv")

    def on_other_feature(self):
        messagebox.showinfo("Coming Soon", "This area is reserved for future features.")


def launch_tkinter_gui():
    app = TimetableApp()
    app.resizable(True, True)
    app.mainloop()


if __name__ == "__main__":
    launch_tkinter_gui()
