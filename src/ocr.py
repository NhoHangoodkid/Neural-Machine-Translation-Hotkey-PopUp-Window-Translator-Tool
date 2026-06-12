"""
Chup vung man hinh -> OCR bang PaddleOCR -> tra ve text.

PaddleOCR duoc load MOT LAN (giong TranslationEngine),
moi lan goi chi chay inference -> nhanh hon nhieu so voi khoi tao lai.
"""
import tkinter as tk
import numpy as np
import cv2
from PIL import ImageGrab, ImageTk, ImageEnhance
from rapidocr_onnxruntime import RapidOCR


class OCREngine:
    """Load RapidOCR mot lan, tai su dung xuyen suot app."""

    def __init__(self, lang: str = "en", use_gpu: bool = False):
        print(f"[OCR] Dang load RapidOCR ...")
        self.engine = RapidOCR()
        print("[OCR] San sang.")

    def recognize(self, img) -> str:
        """Nhan PIL Image, tra ve text."""
        # Convert PIL Image (RGB) to BGR for RapidOCR (giong OpenCV)
        img_array = np.array(img)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        result, _ = self.engine(img_bgr)

        if not result:
            return ""

        # result cua RapidOCR co dang list cac tuple: (box, text, score)
        # box la list 4 diem toa do
        lines = []
        for bbox, text, conf in result:
            top_y = min(p[1] for p in bbox)
            left_x = min(p[0] for p in bbox)
            lines.append((top_y, left_x, text))

        # Gom thanh dong: cac box co top_y gan nhau (<15px) = cung dong
        lines.sort(key=lambda x: (x[0], x[1]))
        grouped = []
        current_row = [lines[0]]
        for item in lines[1:]:
            if abs(item[0] - current_row[0][0]) < 15:
                current_row.append(item)
            else:
                current_row.sort(key=lambda x: x[1])  # sap xep trai->phai
                grouped.append(" ".join(t for _, _, t in current_row))
                current_row = [item]
        current_row.sort(key=lambda x: x[1])
        grouped.append(" ".join(t for _, _, t in current_row))

        return "\n".join(grouped)


class ScreenCapture:
    """Cho nguoi dung keo chon vung tren man hinh."""

    def __init__(self):
        self._result = None
        self._center = (0, 0)

    def grab(self):
        """Tra ve (PIL Image, center_x, center_y) hoac (None, 0, 0)."""
        self._result = None
        screenshot = ImageGrab.grab()

        root = tk.Toplevel()
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.configure(cursor="crosshair")

        dimmed = ImageEnhance.Brightness(screenshot).enhance(0.6)
        tk_img = ImageTk.PhotoImage(dimmed)

        canvas = tk.Canvas(root, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=tk_img)
        canvas.image = tk_img  # Giu reference tranh bi garbage collected

        rect_id = None
        start = [0, 0]

        def on_press(e):
            nonlocal rect_id
            start[0], start[1] = e.x, e.y
            rect_id = canvas.create_rectangle(
                e.x, e.y, e.x, e.y,
                outline="#7c4dff", width=2, dash=(6, 4))

        def on_drag(e):
            if rect_id:
                canvas.coords(rect_id, start[0], start[1], e.x, e.y)

        def on_release(e):
            x1, y1 = min(start[0], e.x), min(start[1], e.y)
            x2, y2 = max(start[0], e.x), max(start[1], e.y)
            if (x2 - x1) > 10 and (y2 - y1) > 10:
                self._result = screenshot.crop((x1, y1, x2, y2))
                self._center = ((x1 + x2) // 2, (y1 + y2) // 2)
            root.destroy()

        def on_escape(e):
            root.destroy()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)
        root.bind("<Escape>", on_escape)

        canvas.create_text(
            screenshot.width // 2, 40,
            text="Kéo chọn vùng cần dịch · Esc để hủy",
            fill="#e8eaf6", font=("Segoe UI", 14, "bold"))

        root.wait_window(root)
        return self._result, self._center


def capture_and_ocr(ocr_engine: OCREngine) -> tuple:
    """
    Chup man hinh -> OCR -> tra ve (text, x, y).
    x, y la vi tri giua vung chon de popup hien gan do.
    """
    cap = ScreenCapture()
    img, (cx, cy) = cap.grab()
    if img is None:
        return None, 0, 0

    text = ocr_engine.recognize(img)
    return (text if text else None), cx, cy
