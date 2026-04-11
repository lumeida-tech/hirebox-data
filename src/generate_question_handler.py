from dataclasses import dataclass
from typing import List
from src.question import Question
from src.spi import QuestionGenerator

@dataclass
class GenerateQuestionFromCVCommandHandler:
    cv_content: str
    number_of_question: int = 1

class GenerateQuestionFromCVHandler():

    def __init__(self, question_generator: QuestionGenerator) -> None:
        self.question_generator =question_generator

    async def execute(self, command: GenerateQuestionFromCVCommandHandler)-> List[Question]:
        if command.number_of_question < 1:
            raise Exception("Le nombre de questions ne peut pas être < 1")
        questions = await self.question_generator.generate_questions(context=command.cv_content,number=command.number_of_question)
        return questions
        