from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from src.glm_ai import Z_AI_Question_Generator
from src.generate_question_handler import GenerateQuestionFromCVCommandHandler, GenerateQuestionFromCVHandler
from src.api import GenerateQuestionsFromCVSchema

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Hirebox"}

@app.get("/ping")
async def ping_pong():
    return {"message": "pong", "status": "OK"}


with open("generate_cv_questions_prompt.txt", "r") as prompt_file:
    GENERATE_CV_PROMPT = prompt_file.read()


@app.post("/generate-questions-from-cv")
async def generate_questions_from_cv(data: GenerateQuestionsFromCVSchema):
    question_generator = Z_AI_Question_Generator(GENERATE_CV_PROMPT)
    handler = GenerateQuestionFromCVHandler(question_generator)
    command = GenerateQuestionFromCVCommandHandler(
        number_of_question=data.number,
        cv_content=data.cv_content
    )
    try:
        questions_generated = await handler.execute(command)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    return {"questions": questions_generated}

