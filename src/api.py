from pydantic import BaseModel


class GenerateQuestionsFromCVSchema(BaseModel):
    number: int
    cv_content: str
