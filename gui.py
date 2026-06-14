"""Simple Tkinter timetable editor with a built-in main menu.

This GUI version lives alongside the existing terminal UI. It reads and writes the same
CSV file, with a polished main menu screen that is ready for additional features.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

from pomodoro_timer import PomodoroScreen, configure_styles



CSV_PATH = "timetabledata.csv"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ROW_COUNT = 5

# Dark Mode Color Palette
BG_DARK = "#1e1e1e"
BG_SECONDARY = "#252526"
CARD_DARK = "#2d2d2d"
BORDER_DARK = "#3c3c3c"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#c5c6c7"
PRIMARY = "#676767"
PRIMARY_HOVER = "#838383"
ACCENT = "#10b981"
BUTTONBG = "#969696"
DANGER = "#d9534f"


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
        self.title("Student Study Assistant")
        self.geometry("1000x600")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("TLabel", background=BG_DARK, foreground=TEXT_PRIMARY, font=("Jetbrains Mono", 11))
        self.style.configure(
            "Primary.TButton",
            background=PRIMARY,
            foreground=TEXT_PRIMARY,
            font=("Jetbrains Mono", 10, "bold"),
            borderwidth=4,
            padding=12,
            relief="raised",
        )
        self.style.map("Primary.TButton", background=[("active", PRIMARY_HOVER)])
        self.style.configure(
            "Danger.TButton",
            background=DANGER,
            foreground=TEXT_PRIMARY,
            font=("Jetbrains Mono", 10, "bold"),
            borderwidth=4,
            padding=12,
            relief="raised",
        )
        self.style.map("Danger.TButton", background=[("active", "#a94442")])
        configure_styles(self.style)
        self.style.configure("MenuTitle.TLabel", background=CARD_DARK, foreground=TEXT_PRIMARY, font=("Jetbrains Mono", 26, "bold"))
        self.style.configure("Header.TLabel", background=BG_DARK, foreground=TEXT_PRIMARY, font=("Jetbrains Mono", 22, "bold"))
        self.style.configure("Info.TLabel", background=BG_DARK, foreground=TEXT_SECONDARY, font=("Jetbrains Mono", 11))
        self.style.configure("CardSubtitle.TLabel", background=CARD_DARK, foreground=TEXT_SECONDARY, font=("Jetbrains Mono", 10))

        self.cells = []
        self.data_frame = load_data()

        self.container = tk.Frame(self, bg=BG_DARK)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.button_references = {}  # Store button references for dynamic updates
        self._build_main_menu()
        self._build_editor_screen()
        self._build_pomodoro_screen()
        self.show_frame("menu")
        
        # Bind window resize event for dynamic scaling
        self.bind("<Configure>", self._on_window_resize)

    def _build_main_menu(self):
        frame = tk.Frame(self.container, bg=BG_DARK)

        card = tk.Frame(frame, bg=CARD_DARK, bd=3, relief="solid", highlightbackground=BORDER_DARK, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=16, pady=16)

        title = ttk.Label(card, text="Main Menu", style="MenuTitle.TLabel")
        title.pack(pady=(28, 12))

        button_frame = tk.Frame(card, bg=CARD_DARK)
        button_frame.pack(pady=(0, 24), expand=True, fill="y")

        timetable_button = ttk.Button(
            button_frame,
            text="Open Timetable Editor",
            command=lambda: self.show_frame("editor"),
            style="Primary.TButton",
        )
        timetable_button.pack(pady=8, expand=True, fill="both", padx=20)
        self.button_references["timetable"] = timetable_button

        other_button = ttk.Button(
            button_frame,
            text="Pomodoro Timer",
            command=lambda: self.show_frame("pomodoro"),
            style="Primary.TButton",
        )
        other_button.pack(pady=8, expand=True, fill="both", padx=20)
        self.button_references["other"] = other_button

        quit_button = ttk.Button(
            button_frame,
            text="Exit",
            command=self.destroy,
            style="Primary.TButton",
        )
        quit_button.pack(pady=(16, 0), expand=True, fill="both", padx=20)
        self.button_references["quit"] = quit_button

        self.frames["menu"] = frame

        creds = ttk.Label(card, text="CruzW EuniceF", style="CardSubtitle.TLabel")
        creds.pack(pady=(120, 12))

        team = ttk.Label(card, text="NAISHK Hacks 26", style="CardSubtitle.TLabel")
        team.pack(pady=(50, 12))

    def _on_window_resize(self, event=None):
        """Update button and text sizes dynamically based on window height."""
        if event is None or "menu" not in self.frames:
            return
        
        # Get current window height
        window_height = self.winfo_height()
        if window_height < 100:
            return
        
        # Calculate dynamic font size based on window height (scale between 8 and 14)
        button_font_size = max(8, min(14, int(window_height / 50)))
        
        # Update button styles dynamically
        self.style.configure(
            "Primary.TButton",
            font=("Jetbrains Mono", button_font_size, "bold"),
        )
        self.style.configure(
            "Danger.TButton",
            font=("Jetbrains Mono", button_font_size, "bold"),
        )
        self.style.configure(
            "Timer.TLabel",
            font=("Jetbrains Mono", max(32, min(72, int(window_height / 8))), "bold"),
        )

    def _build_editor_screen(self):
        frame = tk.Frame(self.container, bg=BG_DARK)

        header_frame = tk.Frame(frame, bg=BG_DARK)
        header_frame.pack(fill="x", pady=(0, 20))

        back_button = ttk.Button(
            header_frame,
            text="Back to Menu",
            command=lambda: self.show_frame("menu"),
            style="Primary.TButton",
        )
        back_button.pack(side="left")

        title_label = ttk.Label(header_frame, text="Timetable Editor", style="Header.TLabel")
        title_label.pack(side="left", padx=16)

        info_label = ttk.Label(frame, text="Click to edit your timetable. Save your changes!", style="Info.TLabel")
        info_label.pack(pady=(0, 14))

        table_card = tk.Frame(frame, bg=CARD_DARK, bd=3, relief="solid", highlightbackground=BORDER_DARK, highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=4, pady=(0, 18))

        self._build_table(table_card)
        self._build_buttons(frame)
        self._refresh_table_values()

        self.frames["editor"] = frame

    def _build_pomodoro_screen(self):
        frame = PomodoroScreen(self.container, on_back=lambda: self.show_frame("menu"))
        self.frames["pomodoro"] = frame

    def _build_table(self, parent):
        self.cells = []
        self.data_frame = load_data()

        # Single unified table frame for proper alignment
        table_frame = tk.Frame(parent, bg=CARD_DARK)
        table_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Configure column and row weights for even distribution
        for col in range(len(DAYS)):
            table_frame.grid_columnconfigure(col, weight=1)
        for row in range(len(self.data_frame) + 1):
            table_frame.grid_rowconfigure(row, weight=1)

        # Header row
        for col, day in enumerate(DAYS):
            label = tk.Label(
                table_frame,
                text=day,
                font=("Jetbrains Mono", 15, "bold"),
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
                    font=("Jetbrains Mono", 11),
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
            text="Save",
            command=self.on_save,
            style="Primary.TButton",
        )
        save_button.grid(row=0, column=0, padx=8, pady=8)

        clear_button = ttk.Button(
            button_frame,
            text="Clear All",
            command=self.on_clear,
            style="Danger.TButton",
        )
        clear_button.grid(row=0, column=1, padx=8, pady=8)

        reload_button = ttk.Button(
            button_frame,
            text="Reload",
            command=self.on_reload,
            style="Primary.TButton",
        )
        reload_button.grid(row=0, column=2, padx=8, pady=8)

        close_button = ttk.Button(
            button_frame,
            text="Exit",
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
        self.frames[name].update_idletasks()

    def _refresh_table_values(self):
        self.data_frame = load_data()
        for row, row_vars in enumerate(self.cells):
            for col, cell_var in enumerate(row_vars):
                cell_var.set(self.data_frame.at[row, DAYS[col]])

    def on_save(self):
        values = [[cell.get().strip() for cell in row] for row in self.cells]
        save_data(values)
        messagebox.showinfo("SAVED", "Timetable Saved Successfully!")

    def on_clear(self):
        if not messagebox.askyesno("CLEAR ALL", "This will clear your data, which cannot be undone."):
            return

        for row_vars in self.cells:
            for cell in row_vars:
                cell.set("")

        self.on_save()

    def on_reload(self):
        self._refresh_table_values()
        messagebox.showinfo("RELOADED", "Timetable Reloaded!")

def launch_tkinter_gui():
    app = TimetableApp()
    app.resizable(True, True)
    app.mainloop()


if __name__ == "__main__":
    launch_tkinter_gui()
