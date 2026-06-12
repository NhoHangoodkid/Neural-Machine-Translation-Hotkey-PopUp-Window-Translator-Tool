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

# Mot cau ket thuc bang . ! ? (co the kem dau dong/ngoac), theo sau la khoang trang.
# Dung de tach cau MA VAN giu nguyen dau cau o cuoi moi cau.
_SENT_BOUNDARY = re.compile(r'(?<=[.!?])["\')\]]?\s+')


def get_selected_text() -> str:
    """Tra ve text dang boi den, hoac chuoi rong neu khong lay duoc."""
    backup = ""
    try:
        backup = pyperclip.paste()
    except Exception:
        pass

    try:
        pyperclip.copy("")
    except Exception:
        pass

    for k in [Key.shift, Key.shift_r, Key.alt, Key.alt_gr, Key.alt_r,
              Key.cmd, Key.cmd_r, Key.ctrl, Key.ctrl_r]:
        _kbd.release(k)

    time.sleep(0.05)

    _kbd.press(Key.ctrl)
    _kbd.press("c")
    _kbd.release("c")
    _kbd.release(Key.ctrl)

    time.sleep(0.15)

    try:
        selected = pyperclip.paste()
    except Exception:
        selected = ""

    try:
        pyperclip.copy(backup)
    except Exception:
        pass

    return selected.strip()


def split_sentences(text: str):
    """
    Tach doan thanh danh sach cau HOAN CHINH (con giu dau cau cuoi).

    Nguyen tac: chi tach theo ranh gioi cau that su (sau . ! ? + khoang trang)
    va theo xuong dong. KHONG cat giua cau, KHONG vut bo dau cau.
    Nho vay moi phan tu tra ve la mot cau dung nghia -> mo hinh dich viet hoa
    dau cau mot cach hop le, khong sinh chu hoa lo lung giua cau khi ghep lai.

    Viec gop cau ngan / chia cau qua dai theo gioi han token do engine lo,
    de capture.py khong phu thuoc vao tokenizer cu the.
    """
    text = text.strip()
    if not text:
        return []

    # Fix loi cat tu: neu co dau gach ngang o cuoi dong (vd: dimen-\nsion), noi chung lai voi nhau
    text = re.sub(r'-[ \t]*\n[ \t]*', '', text)

    sentences = []
    # Tach theo dong truoc, roi tach cau trong tung dong.
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        for part in _SENT_BOUNDARY.split(line):
            part = part.strip()
            if part:
                sentences.append(part)
    return sentences