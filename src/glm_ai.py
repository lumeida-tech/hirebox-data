import os
from openai import OpenAI
from pydantic import BaseModel
from src.spi import Question, QuestionGenerator
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)



class QuestionModel(BaseModel):
    title: str
    question_body: str
    applicant_name: str


def load_cv_content(cv_file_name: str) -> str:
    with open(cv_file_name, "r", encoding="utf-8") as cv_file:
        return cv_file.read()



class Z_AI_Question_Generator(QuestionGenerator):
    def __init__(self, prompt: str) -> None:
        self.__prompt = prompt
        self.__model = "zai-org/GLM-5.1:together"

    async def generate_question(self, cv_content: str) -> Question:
        """
        Génère une seule question à partir du CV fourni.
        """

        system_prompt = (
            "Tu es un recruteur expert. "
            "À partir du CV fourni, génère UNE seule question pertinente "
            "pour tester le candidat lors d'un entretien."
        )

        user_message = (
            f"{self.__prompt}\n\n"
            f"Contenu du CV :\n{cv_content}"
        )

        completion = client.beta.chat.completions.parse(
            model=self.__model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            response_format=QuestionModel,
        )

        parsed: QuestionModel = completion.choices[0].message.parsed  # type: ignore

        return Question(
            title=parsed.title,
            number=1,
            body=parsed.question_body.replace("\n", ""),
            applicant_full_name=parsed.applicant_name,
        )
    
