# Desktop Translator (EN->VI)

A convenient Desktop translation tool (English to Vietnamese). Translate highlighted text anywhere on your Windows system using a global hotkey, and the result will instantly appear in a small popup near your mouse cursor. Additionally, the tool supports Optical Character Recognition (OCR) to extract and translate text from screenshots.

## Technologies & Libraries Used

This project is built and optimized for speed using open-source technologies:

- **Translation Model:** [MarianMT](https://huggingface.co/docs/transformers/model_doc/marian) (`opus-mt-en-vi`) fine-tuned on the MTet dataset and Academic (custom by myself).
- **Inference Engine:** [CTranslate2](https://github.com/OpenNMT/CTranslate2) combined with Hugging Face `transformers` for ultra-fast and lightweight inference (int8 quantization).
- **Optical Character Recognition (OCR):** [RapidOCR](https://github.com/RapidAI/RapidOCR) (`rapidocr_onnxruntime` version), combined with `OpenCV` (`cv2`) and `Pillow` for image processing and text extraction.
- **User Interface (UI):** `tkinter` for smooth popup windows and screen selection overlays.
- **System Interaction:** `pynput` for capturing global hotkeys, `pyperclip` for clipboard operations, and `ctypes` for DPI awareness (preventing blurriness on high-resolution screens).

## Installation

Ensure you have Python 3.8 or higher installed.

```bash
pip install -r requirements.txt
```
*(Note: You may also need to install OCR-related libraries such as `rapidocr_onnxruntime`, `opencv-python`, and `Pillow` if they are not already available)*

## Step 1: Convert the Model

After downloading the output from Kaggle or your trained model and extracting it (e.g., a `final_model/` directory):

```bash
python scripts/convert_to_ct2.py --model path/to/final_model
```

This command will convert the model and create the necessary configuration directories: `models/en-vi-ct2/` and `models/tokenizer-en-vi/`.

## Step 2: Run the App

Launch the application with the following command:

```bash
python src/main.py
```

### Usage
- **Text Translation:** Highlight any text → press **Ctrl+Shift+F** → the translation will appear.
- **OCR Translation:** Press the OCR hotkey (configured in `config.yaml`) → Drag your mouse to select a text area on the screen. The app will scan and translate the text. Press **Esc** to cancel.
- **Exit:** Close the running terminal window to exit the app.

## Extended Features

- **Long Text Translation:** The application automatically splits long paragraphs into individual sentences for smooth translation, preventing truncation at the 128-token limit.
- **Multi-Engine Support:** The `EngineManager` system allows for easy configuration of additional translation directions (VI→EN) or different models.

## License

This project is distributed under the **MIT License**. You are free to use, modify, and distribute it.

## Acknowledgements

This project is built upon several open-source projects and resources:

### Models

* MarianMT (English ↔ Vietnamese Neural Machine Translation)
* Base model: Helsinki-NLP/opus-mt-en-vi
* Fine-tuned on MTET and additional academic-domain parallel corpora

### Open-source Libraries

* Hugging Face Transformers
* CTranslate2
* PyTorch
* RapidOCR
* OpenCV
* Pillow
* pynput
* pyperclip

### References

* Marian NMT: https://github.com/marian-nmt/marian
* Hugging Face Transformers: https://github.com/huggingface/transformers
* CTranslate2: https://github.com/OpenNMT/CTranslate2
* RapidOCR: https://github.com/RapidAI/RapidOCR

Special thanks to the open-source community for providing the tools and resources that made this project possible.
