"""
Popup nho hien ban dich gan con tro chuot.
Dung tkinter (co san trong Python). Chay tren luong chinh (main thread).

Vi tkinter khong an toan khi goi tu luong khac, hotkey listener se gui yeu cau
qua mot hang doi, va vong lap chinh trong main.py se goi show() o day.
"""
import tkinter as tk


class Popup:
    def __init__(self, timeout_ms: int = 9000, font_size: int = 12, max_width: int = 460):
        self.timeout_ms = timeout_ms
        self.font_size = font_size
        self.max_width = max_width
        self.root = tk.Tk()
        self.root.withdraw()  # an cua so goc
        self._win = None

    def show(self, text, x, y):
        # Dong popup cu neu con
        if self._win is not None:
            try:
                self._win.destroy()
            except Exception:
                pass

        win = tk.Toplevel(self.root)
        self._win = win
        win.overrideredirect(True)          # bo vien cua so
        win.attributes("-topmost", True)    # luon noi len tren
        win.configure(bg="#1e1e1e")

        # Vi tri: gan con tro neu co, neu khong thi giua tren cung
        if x is None or y is None:
            x = win.winfo_screenwidth() // 2 - self.max_width // 2
            y = 80
        win.geometry(f"+{x + 12}+{y + 12}")

        frame = tk.Frame(win, bg="#1e1e1e", padx=12, pady=10)
        frame.pack()

        label = tk.Label(
            frame, text=text, bg="#1e1e1e", fg="#eaeaea",
            font=("Segoe UI", self.font_size), justify="left",
            wraplength=self.max_width, anchor="w")
        label.pack()

        hint = tk.Label(
            frame, text="Esc / click de dong", bg="#1e1e1e", fg="#777",
            font=("Segoe UI", 8))
        hint.pack(anchor="e", pady=(6, 0))

        # Dong bang Esc hoac click
        win.bind("<Escape>", lambda e: self._close())
        win.bind("<Button-1>", lambda e: self._close())
        win.focus_force()

        if self.timeout_ms and self.timeout_ms > 0:
            win.after(self.timeout_ms, self._close)

    def show_loading(self, x: int = None, y: int = None):
        self.show("Dang dich...", x, y)

    def _close(self):
        if self._win is not None:
            try:
                self._win.destroy()
            except Exception:
                pass
            self._win = None

    def run_mainloop(self):
        self.root.mainloop()