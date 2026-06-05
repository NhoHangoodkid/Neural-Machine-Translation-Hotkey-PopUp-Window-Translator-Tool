"""
Convert model HuggingFace (PyTorch) tu Kaggle sang dinh dang CTranslate2.

Chay MOT LAN sau khi tai output Kaggle ve va giai nen.
>> Khong thuoc runtime cua app. <<

Cach dung:
    python scripts/convert_to_ct2.py \
        --model  duong_dan/den/final_model \
        --output models/en-vi-ct2 \
        --tokenizer-out models/tokenizer-en-vi

Sau khi chay xong:
    models/en-vi-ct2/        <- model CT2 (model.bin, config.json, ...)
    models/tokenizer-en-vi/  <- file tokenizer (source.spm, vocab, ...)
"""


import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def convert(model_path, output_dir, tokenizer_out, quantization):
    model_path = Path(model_path)
    if not model_path.is_dir():
        sys.exit(f"Khong thay thu muc model: {model_path}")

    output_dir = Path(output_dir)
    if output_dir.exists():
        print(f"{output_dir} da ton tai -> xoa de convert lai")
        shutil.rmtree(output_dir)

    # 1. Convert model sang CTranslate2
    print(f"[1/2] Convert {model_path} -> {output_dir} (quant={quantization})")
    subprocess.run(
        [
            "ct2-transformers-converter",
            "--model", str(model_path),
            "--output_dir", str(output_dir),
            "--quantization", quantization,
        ],
        check=True)

    # 2. Copy file tokenizer
    tokenizer_out = Path(tokenizer_out)
    tokenizer_out.mkdir(parents=True, exist_ok=True)
    tok_files = [
        "source.spm", "target.spm", "vocab.json",
        "tokenizer_config.json", "special_tokens_map.json",
        "config.json"
    ]
    print(f"[2/2] Copy tokenizer -> {tokenizer_out}")
    for name in tok_files:
        src = model_path / name
        if src.exists():
            shutil.copy(src, tokenizer_out / name)
            print(f"      + {name}")

    print("\n[OK] Hoan tat. App co the load tu:")
    print(f"model     = {output_dir}")
    print(f"tokenizer = {tokenizer_out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="Thu muc final_model tu Kaggle")
    ap.add_argument("--output", default="models/en-vi-ct2", help="Thu muc xuat model CT2")
    ap.add_argument("--tokenizer-out", default="models/tokenizer-en-vi", help="Thu muc xuat tokenizer")
    ap.add_argument("--quantization", default="int8", choices=["int8", "int8_float16", "float16", "float32"])
    args = ap.parse_args()
    convert(args.model, args.output, args.tokenizer_out, args.quantization)