from pydantic import BaseModel
from src.question import Question


class GenerateQuestionsFromCVDto(BaseModel):
    question: Question
