from typing import Protocol, List
from src.question import Question


class QuestionGenerator(Protocol):
    async def generate_new_question(self, context: str) -> Question: ...
    async def generate_questions(self, context: str, number: int) -> List[Question]: ...
