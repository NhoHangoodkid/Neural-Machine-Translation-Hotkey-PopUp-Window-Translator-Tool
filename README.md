# Desktop Translator (EN->VI)

Dịch text bôi đen ở bất kỳ đâu trên Windows bằng hotkey toàn cục, kết quả hiện trong popup nhỏ gần con trỏ. Model là MarianMT (`opus-mt-en-vi`) đã fine-tune trên MTet, chạy inference nhanh bằng CTranslate2 (int8).


## Cài đặt

```bash
pip install -r requirements.txt
```

## Bước 1 — Convert model từ Kaggle

Sau khi tải output Kaggle về và giải nén (có thư mục `final_model/`):

```bash
python scripts/convert_to_ct2.py --model duong_dan/den/final_model
```

Lệnh này tạo `models/en-vi-ct2/` và `models/tokenizer-en-vi/`.

## Bước 2 — Chạy app

```bash
python src/main.py
```

Bôi đen text bất kỳ → nhấn **Ctrl+Shift+F** → bản dịch hiện ra. Đóng cửa sổ terminal để thoát.

## Mở rộng sau này

**Thêm OCR:** viết hàm `capture_from_image()` trong `src/capture.py`, thêm hotkey thứ hai trong `config.yaml` và `main.py`. Không đụng tới `engine.py` hay `popup.py`.

**Thêm VI→EN:** convert model VI→EN, bỏ comment phần `vi-en` trong `config.yaml`, thêm phát hiện ngôn ngữ để chọn engine. `EngineManager` đã sẵn sàng giữ nhiều engine.

## Ghi chú

- `max_input_length` trong config phải khớp với lúc train (128).
- App tách đoạn dài thành từng câu rồi dịch, tránh bị cắt cụt ở 128 token.
