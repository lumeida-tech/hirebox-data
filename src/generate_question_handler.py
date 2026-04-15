from dataclasses import dataclass
from src.question import Question
from src.spi import QuestionGenerator


@dataclass
class GenerateQuestionFromCVCommandHandler:
    cv_content: str


class GenerateQuestionFromCVHandler:
    def __init__(self, question_generator: QuestionGenerator) -> None:
        self.question_generator = question_generator

    async def execute(self, command: GenerateQuestionFromCVCommandHandler)-> Question:
        
        question = await self.question_generator.generate_question(cv_content=command.cv_content,)
        return question
        
