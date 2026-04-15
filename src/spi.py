from typing import Protocol
from src.question import Question


class QuestionGenerator(Protocol):
    async def generate_question(self, cv_content: str) -> Question:...