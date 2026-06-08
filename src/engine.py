"""
Engine dich: load model CTranslate2 + tokenizer HuggingFace MOT LAN,
sau do moi lan dich chi goi translate() -> nhanh.

Thiet ke khong hard-code EN->VI: moi engine la mot cap (model, tokenizer).
Them VI->EN sau nay = tao them mot TranslationEngine khac, khong sua logic.

Xu ly do dai: engine tu gom cac cau ngan thanh "lo" vua trong max_input_length
va chi cat nho cau qua dai khi that su can. Capture chi can dua list cau hoan
chinh vao -> tach trach nhiem ro rang, de bao tri.
"""
import ctranslate2
from transformers import AutoTokenizer


class TranslationEngine:
    def __init__(self, model_dir: str, tokenizer_dir: str,
                 device: str = "cpu", max_input_length: int = 128,
                 num_beams: int = 4, max_decode_length: int = 128):
        # Load 1 lan luc khoi dong app
        self.translator = ctranslate2.Translator(model_dir, device=device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
        self.max_input_length = max_input_length
        self.num_beams = num_beams
        self.max_decode_length = max_decode_length

    def _n_tokens(self, text: str) -> int:
        return len(self.tokenizer(text, add_special_tokens=True)["input_ids"])

    def _pack(self, sentences):
        """
        Gom cau hoan chinh thanh cac lo, moi lo <= max_input_length token.
        Cau nao tu no da qua dai thi tach rieng (engine se truncate khi dich).
        Tra ve list[str], moi phan tu la mot doan van ban se dua thang vao model.
        """
        chunks = []
        cur, cur_tok = [], 0
        for s in sentences:
            n = self._n_tokens(s)
            if n >= self.max_input_length:
                # cau qua dai: chot lo hien tai, day cau dai thanh lo rieng
                if cur:
                    chunks.append(" ".join(cur))
                    cur, cur_tok = [], 0
                chunks.append(s)
                continue
            if cur and cur_tok + n > self.max_input_length:
                chunks.append(" ".join(cur))
                cur, cur_tok = [], 0
            cur.append(s)
            cur_tok += n
        if cur:
            chunks.append(" ".join(cur))
        return chunks

    def _translate_one(self, text):
        # HF tokenizer -> token string -> CT2 translate -> ghep lai
        src = self.tokenizer(text, truncation=True, max_length=self.max_input_length)
        tokens = self.tokenizer.convert_ids_to_tokens(src["input_ids"])

        results = self.translator.translate_batch(
            [tokens],
            beam_size=self.num_beams,
            max_decoding_length=self.max_decode_length)

        out_tokens = results[0].hypotheses[0]
        out_ids = self.tokenizer.convert_tokens_to_ids(out_tokens)
        return self.tokenizer.decode(out_ids, skip_special_tokens=True).strip()

    def translate(self, sentences) -> str:
        """
        Nhan 1 cau (str) hoac list cau hoan chinh (list[str]) -> tra ve 1 chuoi.

        Vi moi 'chunk' dua vao model la mot/ nhieu cau hoan chinh (co dau cau),
        ket qua dich co dau cau o ranh gioi -> ghep bang khoang trang la dung,
        khong con chu hoa lo lung giua cau.
        """
        if isinstance(sentences, str):
            sentences = [sentences]
        sentences = [s.strip() for s in sentences if s and s.strip()]
        if not sentences:
            return ""

        chunks = self._pack(sentences)
        parts = [self._translate_one(c) for c in chunks]
        return " ".join(p for p in parts if p).strip()


class EngineManager:
    """Quan ly nhieu engine, chon theo cap ngon ngu. Hien tai chi co en-vi."""

    def __init__(self):
        self._engines = {}
        self._default = None

    def register(self, name: str, engine: TranslationEngine,
                 is_default: bool = False):
        self._engines[name] = engine
        if is_default or self._default is None:
            self._default = name

    def translate(self, sentences, engine_name: str = None) -> str:
        name = engine_name or self._default
        if name not in self._engines:
            raise KeyError(f"Chua co engine '{name}'")
        return self._engines[name].translate(sentences)