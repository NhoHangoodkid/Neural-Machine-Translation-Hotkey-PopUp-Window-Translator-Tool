"""
Dang ky va lang nghe hotkey toan cuc bang pynput.

Khi nguoi dung nhan hotkey, chi day mot "su kien" vao hang doi.
Viec dich + hien popup do main.py xu ly tren luong chinh (tkinter yeu cau vay).
"""
from pynput import keyboard


def parse_hotkey(hotkey_str: str) -> str:
    """ 'ctrl+shift+c' -> dinh dang pynput '<ctrl>+<shift>+c' """
    mods = {"ctrl": "<ctrl>", "shift": "<shift>", "alt": "<alt>",
            "cmd": "<cmd>", "win": "<cmd>"}
    keys = []
    for k in hotkey_str.lower().split("+"):
        k = k.strip()
        keys.append(mods.get(k, k))
    return "+".join(keys)


class HotkeyListener:
    def __init__(self, hotkey_str: str, on_trigger):
        """on_trigger: ham khong tham so, goi khi nhan hotkey."""
        self.combo = parse_hotkey(hotkey_str)
        self.on_trigger = on_trigger
        self._listener = None

    def start(self):
        self._listener = keyboard.GlobalHotKeys({self.combo: self.on_trigger})
        self._listener.start()  # chay tren luong rieng

    def stop(self):
        if self._listener is not None:
            self._listener.stop()