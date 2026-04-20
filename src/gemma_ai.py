# type: ignore

import json
import os
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor
import torch
from transformers import AutoTokenizer, Gemma4ForConditionalGeneration, BitsAndBytesConfig  # type: ignore
from src.spi import QuestionGenerator
from src.question import Question

from dotenv import load_dotenv
load_dotenv()

MODEL_PATH = os.getenv("GEMMA_MODEL_PATH", "models/google/gemma-4-E2B-it")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "150"))
CV_MAX_TOKENS = int(os.getenv("CV_MAX_TOKENS", "600"))

SYSTEM_PROMPT = (
    "Tu es un recruteur expert. "
    "À partir du CV fourni, génère UNE seule question d'entretien pertinente. "
    'Réponds UNIQUEMENT en JSON valide : {"title": "...", "question": "..."}. '
    "Texte brut uniquement. Pas de HTML. Pas de markdown. Rien d'autre que le JSON."
)

_WARMUP_CV = "Développeur Python, 3 ans d'expérience, Django, FastAPI."


def _build_model() -> Gemma4ForConditionalGeneration:
    try:
        import flash_attn  # noqa: F401
        attn_impl = "flash_attention_2"
    except ImportError:
        attn_impl = "sdpa"

    if torch.cuda.is_available():
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )
        model = Gemma4ForConditionalGeneration.from_pretrained(
            MODEL_PATH,
            quantization_config=quantization_config,
            device_map="auto",
            attn_implementation=attn_impl,
        )
    else:
        model = Gemma4ForConditionalGeneration.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            attn_implementation=attn_impl,
        )

    model.eval()

    if torch.cuda.is_available():
        model = torch.compile(model, mode="reduce-overhead")  # type: ignore

    return model  # type: ignore


class Gemma_Question_Generator(QuestionGenerator):
    _executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)

    def __init__(self, prompt: str) -> None:
        self.__prompt = prompt
        self.__tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.__model = _build_model()
        self._warmup()

    def _truncate_cv(self, cv_content: str) -> str:
        tokens = self.__tokenizer.encode(cv_content, add_special_tokens=False)
        if len(tokens) <= CV_MAX_TOKENS:
            return cv_content
        return self.__tokenizer.decode(tokens[:CV_MAX_TOKENS], skip_special_tokens=True)

    def _run_inference(self, cv_content: str) -> str:
        cv_content = self._truncate_cv(cv_content)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{self.__prompt}\n\nContenu du CV :\n{cv_content}"},
        ]

        inputs = self.__tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.__model.device)

        input_len = inputs["input_ids"].shape[-1]

        with torch.no_grad():
            output_ids = self.__model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=True,
                temperature=0.8,
                top_p=0.95,
                pad_token_id=self.__tokenizer.eos_token_id,
            )

        return self.__tokenizer.decode(output_ids[0][input_len:], skip_special_tokens=True)

    def _warmup(self) -> None:
        try:
            self._run_inference(_WARMUP_CV)
        except Exception:
            pass

    async def generate_question(self, cv_content: str) -> Question:
        loop = asyncio.get_event_loop()
        raw_text: str = await loop.run_in_executor(
            self._executor, self._run_inference, cv_content
        )

        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if not match:
            raise ValueError(
                f"Impossible d'extraire le JSON de la réponse : {raw_text}")

        data: dict[str, str] = json.loads(match.group())

        return Question(
            title=data["title"],
            number=1,
            body=data["question"],
            applicant_full_name="",
        )
