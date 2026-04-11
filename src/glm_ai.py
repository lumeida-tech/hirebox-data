from typing import List

from src.spi import Question, QuestionGenerator

# Docs: https://huggingface.co/docs/transformers/main/en/model_doc/glm_moe_dsa#transformers.GlmMoeDsaForCausalLM

# Docs: https://huggingface.co/docs/transformers/main_classes/pipelines

class Z_AI_Question_Generator(QuestionGenerator):
    def __init__(self, prompt: str) -> None:
        self.__prompt = prompt
    async def generate_new_question(self, context: str) -> Question:
        """
            Implementer la generation d une seul question
        """
        raise NotImplementedError("Veuillez implementer cette methode!")
    
    async def generate_questions(self, context: str, number: int) -> List[Question]:
        """
            Implementer la generation d une seul question à partir du self.__prompt
        """
        raise NotImplementedError("Veuillez implementer cette methode!")
    


    