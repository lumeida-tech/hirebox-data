import json
import os
import re
import torch
from transformers import AutoTokenizer, Gemma4ForConditionalGeneration  # type: ignore
from src.spi import QuestionGenerator
from src.question import Question

from dotenv import load_dotenv
load_dotenv()

MODEL_PATH = os.getenv("GEMMA_MODEL_PATH", "models/google/gemma-4-E2B-it")


class Gemma_Question_Generator(QuestionGenerator):
    def __init__(self, prompt: str) -> None:
        self.__prompt = prompt
        self.__tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.__model = Gemma4ForConditionalGeneration.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.bfloat16,
        )

    async def generate_question(self, cv_content: str) -> Question:
        system_prompt = (
            "Tu es un recruteur expert. "
            "À partir du CV fourni, génère UNE seule question pertinente "
            "pour tester le candidat lors d'un entretien. "
            "Réponds UNIQUEMENT en JSON valide avec exactement ces champs : "
            "title, question_body, applicant_name. "
            "N'ajoute aucun texte en dehors du JSON."
        )

        user_message = (
            f"{self.__prompt}\n\n"
            f"Contenu du CV :\n{cv_content}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        inputs = self.__tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.__model.device)

        with torch.no_grad():
            output_ids = self.__model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=1.0,
                top_p=0.95,
                top_k=64,
                do_sample=True,
            )

        input_len = inputs["input_ids"].shape[-1]
        raw_text: str = self.__tokenizer.decode(
            output_ids[0][input_len:], skip_special_tokens=True
        )

        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if not match:
            raise ValueError(
                f"Impossible d'extraire le JSON de la réponse : {raw_text}"
            )

        data: dict[str, str] = json.loads(match.group())

        return Question(
            title=data["title"],
            number=1,
            body=data["question_body"].replace("\n", "").replace('\\"', ""),
            applicant_full_name=data["applicant_name"],
        )
