
from pydantic import BaseModel
from src.question import Question


class GenerateQuestionsFromCVSchema(BaseModel):
    cv_content: str="Contenu texte du CV."


class GenerateQuestionsFromCVDto(BaseModel):
    question: Question