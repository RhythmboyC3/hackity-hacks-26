# Credit to EuniceF for this base code

import tkinter as tk
from tkinter import ttk

work_time = 25 * 60
break_time = 5 * 60
long_break_time = 15 * 60

BG_DARK = "#1e1e1e"
BG_SECONDARY = "#252526"
CARD_DARK = "#2d2d2d"
BORDER_DARK = "#3c3c3c"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#c5c6c7"
PRIMARY = "#676767"
PRIMARY_HOVER = "#838383"
ACCENT = "#10b981"
DANGER = "#d9534f"


def configure_styles(style):
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TLabel", background=BG_DARK, foreground=TEXT_PRIMARY, font=("Jetbrains Mono", 11))
    style.configure("Card.TLabel", background=CARD_DARK, foreground=TEXT_PRIMARY, font=("Jetbrains Mono", 11))
    style.configure("Timer.TLabel", background=BG_DARK, foreground=ACCENT, font=("Jetbrains Mono", 56, "bold"))
    style.configure("Header.TLabel", background=BG_DARK, foreground=TEXT_PRIMARY, font=("Jetbrains Mono", 22, "bold"))
    style.configure("Info.TLabel", background=BG_DARK, foreground=TEXT_SECONDARY, font=("Jetbrains Mono", 11))
    style.configure("CardSubtitle.TLabel", background=CARD_DARK, foreground=TEXT_SECONDARY, font=("Jetbrains Mono", 10))
    style.configure(
        "Primary.TButton",
        background=PRIMARY,
        foreground=TEXT_PRIMARY,
        font=("Jetbrains Mono", 10, "bold"),
        borderwidth=4,
        padding=12,
        relief="raised",
    )
    style.map("Primary.TButton", background=[("active", PRIMARY_HOVER)])
    style.configure(
        "Danger.TButton",
        background=DANGER,
        foreground=TEXT_PRIMARY,
        font=("Jetbrains Mono", 10, "bold"),
        borderwidth=4,
        padding=12,
        relief="raised",
    )
    style.map("Danger.TButton", background=[("active", "#a94442")])
    style.configure("TNotebook", background=BG_DARK, borderwidth=0, tabmargins=[2, 6, 2, 0])
    style.configure(
        "TNotebook.Tab",
        background=BG_SECONDARY,
        foreground=TEXT_PRIMARY,
        padding=[16, 8],
        font=("Jetbrains Mono", 10, "bold"),
    )
    style.map("TNotebook.Tab", background=[("selected", CARD_DARK)], foreground=[("selected", ACCENT)])
    style.configure("TFrame", background=BG_DARK)


class PomodoroScreen(tk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent, bg=BG_DARK)
        self.on_back = on_back

        self.pomodoros = 0
        self.stopped = True
        self.paused = False
        self.skipped = False
        self.remaining = work_time
        self._after_id = None

        self._build_ui()

    def _build_ui(self):
        header_frame = tk.Frame(self, bg=BG_DARK)
        header_frame.pack(fill="x", pady=(0, 20))

        if self.on_back is not None:
            back_button = ttk.Button(
                header_frame,
                text="Back to Menu",
                command=self._on_back,
                style="Primary.TButton",
            )
            back_button.pack(side="left")

        title_label = ttk.Label(header_frame, text="Pomodoro Timer", style="Header.TLabel")
        title_label.pack(side="left", padx=16 if self.on_back else 0)

        info_label = ttk.Label(
            self,
            text="Focus in 25-minute blocks, then take a short break. Every 4th break is longer.",
            style="Info.TLabel",
        )
        info_label.pack(pady=(0, 14))

        card = tk.Frame(
            self,
            bg=CARD_DARK,
            bd=3,
            relief="solid",
            highlightbackground=BORDER_DARK,
            highlightthickness=1,
        )
        card.pack(fill="both", expand=True, padx=4, pady=(0, 18))

        self.tabs = ttk.Notebook(card)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=16)

        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.pomodoro_timer_label = ttk.Label(self.tab1, text="25:00", style="Timer.TLabel")
        self.pomodoro_timer_label.pack(expand=True, pady=40)

        self.break_timer_label = ttk.Label(self.tab2, text="05:00", style="Timer.TLabel")
        self.break_timer_label.pack(expand=True, pady=40)

        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", style="Timer.TLabel")
        self.long_break_timer_label.pack(expand=True, pady=40)

        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Break")
        self.tabs.add(self.tab3, text="Long Break")

        creds = ttk.Label(card, text="CruzW EuniceF", style="CardSubtitle.TLabel")
        creds.pack(pady=(0, 8))

        team = ttk.Label(card, text="NAISHK Hacks 26", style="CardSubtitle.TLabel")
        team.pack(pady=(0, 12))

        button_frame = tk.Frame(self, bg=BG_DARK)
        button_frame.pack(pady=(8, 0))

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer, style="Primary.TButton")
        self.start_button.grid(row=0, column=0, padx=8, pady=8)

        self.pause_button = ttk.Button(
            button_frame, text="Pause", command=self.toggle_pause, style="Primary.TButton", state="disabled"
        )
        self.pause_button.grid(row=0, column=1, padx=8, pady=8)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer, style="Danger.TButton")
        self.reset_button.grid(row=0, column=2, padx=8, pady=8)

        self.skip_button = ttk.Button(button_frame, text="Skip", command=self.skip_timer, style="Primary.TButton")
        self.skip_button.grid(row=0, column=3, padx=8, pady=8)

        self.pomodoro_counter_label = ttk.Label(button_frame, text="Pomodoros: 0", style="Info.TLabel")
        self.pomodoro_counter_label.grid(row=1, column=0, columnspan=4, pady=10)

    def _on_back(self):
        self._cancel_tick()
        self._set_running_state(False)
        if self.on_back is not None:
            self.on_back()

    def _current_mode(self):
        return self.tabs.index(self.tabs.select())

    def _select_tab(self, mode):
        tab = (self.tab1, self.tab2, self.tab3)[mode]
        self.tabs.select(tab)
        self.update_idletasks()

    def _break_mode_after_work(self):
        return 2 if self.pomodoros % 4 == 0 else 1

    def _label_for_mode(self, mode):
        if mode == 0:
            return self.pomodoro_timer_label
        if mode == 1:
            return self.break_timer_label
        return self.long_break_timer_label

    def _duration_for_mode(self, mode):
        if mode == 0:
            return work_time
        if mode == 1:
            return break_time
        return long_break_time

    def _format_time(self, seconds):
        minutes, secs = divmod(seconds, 60)
        return f"{minutes:02d}:{secs:02d}"

    def _update_display(self, mode=None, seconds=None):
        mode = self._current_mode() if mode is None else mode
        seconds = self.remaining if seconds is None else seconds
        self._label_for_mode(mode).config(text=self._format_time(seconds))

    def _cancel_tick(self):
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _set_running_state(self, running):
        if running:
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal", text="Pause" if not self.paused else "Resume")
        else:
            self.paused = False
            self.start_button.config(state="normal")
            self.pause_button.config(state="disabled", text="Pause")

    def start_timer(self, *, mode=None, reset=True):
        self._cancel_tick()
        self.stopped = False
        self.skipped = False
        self.paused = False

        active_mode = mode if mode is not None else self._current_mode()
        if mode is not None:
            self._select_tab(mode)
        if reset:
            self.remaining = self._duration_for_mode(active_mode)

        self._set_running_state(True)
        self._update_display(active_mode)
        self._tick()

    def toggle_pause(self):
        if self.stopped and not self.paused:
            return

        if self.paused:
            self.paused = False
            self.stopped = False
            self.pause_button.config(text="Pause")
            self.start_button.config(state="disabled")
            self._tick()
            return

        self.paused = True
        self.stopped = True
        self._cancel_tick()
        self.pause_button.config(text="Resume")
        self.start_button.config(state="disabled")

    def _tick(self):
        if self.stopped or self.paused:
            return

        self._update_display()

        if self.remaining <= 0:
            self._on_timer_complete()
            return

        self.remaining -= 1
        self._after_id = self.after(1000, self._tick)

    def _on_timer_complete(self):
        mode = self._current_mode()

        if mode == 0:
            self.pomodoros += 1
            self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")
            next_mode = self._break_mode_after_work()
        else:
            next_mode = 0

        if not self.stopped and not self.skipped:
            self.start_timer(mode=next_mode, reset=True)
        else:
            self._select_tab(next_mode)
            self._update_display(next_mode, self._duration_for_mode(next_mode))

    def reset_timer(self):
        self._cancel_tick()
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self._set_running_state(False)
        self.pomodoro_counter_label.config(text="Pomodoros: 0")
        self.pomodoro_timer_label.config(text="25:00")
        self.break_timer_label.config(text="05:00")
        self.long_break_timer_label.config(text="15:00")
        self._select_tab(0)

    def skip_timer(self):
        self._cancel_tick()
        self.stopped = True
        self.skipped = True
        self._set_running_state(False)

        mode = self._current_mode()
        if mode == 0:
            next_mode = self._break_mode_after_work()
        else:
            next_mode = 0

        self._select_tab(next_mode)
        self._update_display(next_mode, self._duration_for_mode(next_mode))


class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Study Assistant — Pomodoro")
        self.geometry("1000x600")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        self.style = ttk.Style(self)
        configure_styles(self.style)

        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        PomodoroScreen(container).pack(fill="both", expand=True)

        self.bind("<Configure>", self._on_window_resize)
        self.mainloop()

    def _on_window_resize(self, event=None):
        if event is None or event.widget is not self:
            return

        window_height = self.winfo_height()
        if window_height < 100:
            return

        button_font_size = max(8, min(14, int(window_height / 50)))
        timer_font_size = max(32, min(72, int(window_height / 8)))

        self.style.configure("Primary.TButton", font=("Jetbrains Mono", button_font_size, "bold"))
        self.style.configure("Danger.TButton", font=("Jetbrains Mono", button_font_size, "bold"))
        self.style.configure("Timer.TLabel", font=("Jetbrains Mono", timer_font_size, "bold"))


def launch_pomodoro_gui():
    PomodoroApp()


if __name__ == "__main__":
    launch_pomodoro_gui()
