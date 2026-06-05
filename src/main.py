"""
Entry point cua app dich.

Luong hoat dong:
  1. Doc config, load engine (CTranslate2) MOT LAN
  2. Dang ky hotkey toan cuc tren luong rieng
  3. Khi nhan hotkey -> day su kien vao hang doi
  4. Vong lap tkinter o luong chinh kiem tra hang doi -> lay text -> dich -> popup

Vi sao co hang doi: tkinter chi an toan khi goi tu luong chinh, con pynput
goi callback tu luong rieng. Hang doi la cau noi an toan giua hai luong.
"""
import queue
import sys
from pathlib import Path

import yaml
from pynput.mouse import Controller as MouseController

# Cho phep import module trong cung thu muc src/
sys.path.insert(0, str(Path(__file__).parent))

from engine import TranslationEngine, EngineManager   
from capture import get_selected_text, split_sentences  
from popup import Popup                                  
from hotkey import HotkeyListener                       

ROOT = Path(__file__).parent.parent


def load_config():
    with open(ROOT / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_engine_manager(cfg) -> EngineManager:
    mgr = EngineManager()
    t = cfg["translation"]
    default_name = cfg["engines"]["default"]

    for name, spec in cfg["engines"].items():
        if name == "default":
            continue
        model_dir = ROOT / spec["model_dir"]
        tok_dir = ROOT / spec["tokenizer_dir"]
        if not model_dir.is_dir():
            print(f"Bo qua engine '{name}': khong thay {model_dir}")
            continue
        print(f"Load engine '{name}' tu {model_dir} ...")
        eng = TranslationEngine(
            model_dir=str(model_dir),
            tokenizer_dir=str(tok_dir),
            device=cfg["device"],
            max_input_length=t["max_input_length"],
            num_beams=t["num_beams"],
            max_decode_length=t["max_decode_length"])
        mgr.register(name, eng, is_default=(name == default_name))
    return mgr


def main():
    cfg = load_config()

    mgr = build_engine_manager(cfg)
    if mgr._default is None:
        sys.exit("Khong load duoc engine nao. Kiem tra thu muc models/ "
                 "va da chay convert_to_ct2.py chua.")

    ui = cfg["ui"]
    popup = Popup(timeout_ms=ui["popup_timeout_ms"], font_size=ui["font_size"], max_width=ui["max_width"])
    mouse = MouseController()

    # Hang doi noi luong hotkey -> luong chinh (tkinter)
    events = queue.Queue()

    def on_hotkey():
        events.put("translate")

    listener = HotkeyListener(cfg["hotkeys"]["translate_selection"], on_hotkey)
    listener.start()

    print(f"\n[OK] San sang. Boi den text bat ky roi nhan "
          f"{cfg['hotkeys']['translate_selection'].upper()} de dich.")
    print("Dong cua so terminal nay de thoat app.\n")

    def process_queue():
        try:
            while True:
                events.get_nowait()
                handle_translate()
        except queue.Empty:
            pass
        # Kiem tra lai sau 80ms
        popup.root.after(80, process_queue)

    def handle_translate():
        text = get_selected_text()
        x, y = mouse.position
        if not text:
            popup.show("Khong lay duoc text boi den.", x, y)
            return
        popup.show_loading(x, y)
        popup.root.update_idletasks()
        try:
            sentences = split_sentences(text)
            result = mgr.translate(sentences)
            popup.show(result or "(khong co ket qua)", x, y)
        except Exception as e:
            popup.show(f"Loi dich: {e}", x, y)

    popup.root.after(80, process_queue)
    try:
        popup.run_mainloop()
    finally:
        listener.stop()


if __name__ == "__main__":
    main()