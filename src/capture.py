"""
Lay text dang boi den: backup clipboard -> gia lap Ctrl+C -> doc clipboard
-> tra clipboard cu lai. Co tach cau cho doan dai.

OCR sau nay: them ham capture_from_image() vao day, tra ve cung kieu str.
"""
import re
import time

import pyperclip
from pynput.keyboard import Controller, Key

_kbd = Controller()


def get_selected_text() -> str:
    """Tra ve text dang boi den, hoac chuoi rong neu khong lay duoc."""
    backup = ""
    try:
        backup = pyperclip.paste()
    except Exception:
        pass

    # Xoa clipboard de phat hien truong hop khong copy duoc gi
    try:
        pyperclip.copy("")
    except Exception:
        pass

    # Giai phong cac phim modifier (tranh truong hop nguoi dung dang giu Shift -> thanh Ctrl+Shift+F)
    for k in [Key.shift, Key.shift_r, Key.alt, Key.alt_gr, Key.alt_r, Key.cmd, Key.cmd_r, Key.ctrl, Key.ctrl_r]:
        _kbd.release(k)
        
    time.sleep(0.05)

    # Gia lap Ctrl+C
    _kbd.press(Key.ctrl)
    _kbd.press("c")
    _kbd.release("c")
    _kbd.release(Key.ctrl)

    # Cho he dieu hanh cap nhat clipboard
    time.sleep(0.15)

    try:
        selected = pyperclip.paste()
    except Exception:
        selected = ""

    # Tra clipboard cu lai cho nguoi dung
    try:
        pyperclip.copy(backup)
    except Exception:
        pass

    return selected.strip()


def split_sentences(text: str):
    """Tach doan dai thanh cau de khong vuot max_input_length khi dich."""
    text = text.strip()
    if not text:
        return []
    # Tach theo . ! ? va xuong dong; giu lai dau cau
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p.strip() for p in parts if p.strip()]