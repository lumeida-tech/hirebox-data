from dotenv import load_dotenv


from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import os
from src.glm_ai import Z_AI_Question_Generator
from src.generate_question_handler import GenerateQuestionFromCVCommandHandler, GenerateQuestionFromCVHandler
from src.api import GenerateQuestionsFromCVDto, GenerateQuestionsFromCVSchema

load_dotenv()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Hirebox"}

@app.get("/ping")
async def ping_pong():
    return {"message": "pong", "status": "OK"}

GENERATE_CV_QUESTION_PROMPT_FILE=os.getenv("GENERATE_CV_QUESTION_PROMPT_FILE", "")
with open(GENERATE_CV_QUESTION_PROMPT_FILE, "r") as prompt_file:
    GENERATE_CV_PROMPT = prompt_file.read()


@app.post("/generate-question-from-cv", response_model=GenerateQuestionsFromCVDto)
async def generate_questions_from_cv(data: GenerateQuestionsFromCVSchema):
    question_generator = Z_AI_Question_Generator(GENERATE_CV_PROMPT)
    handler = GenerateQuestionFromCVHandler(question_generator)
    command = GenerateQuestionFromCVCommandHandler(
        cv_content=data.cv_content  
    )
    try:
        question_generated = await handler.execute(command)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    return GenerateQuestionsFromCVDto(question=question_generated)

