from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
import os
from scalar_fastapi import get_scalar_api_reference
from src.glm_ai import Z_AI_Question_Generator
# from src.gemma_ai import Gemma_Question_Generator
from src.generate_question_handler import GenerateQuestionFromCVCommandHandler, GenerateQuestionFromCVHandler
from src.api import GenerateQuestionsFromCVDto, GenerateQuestionsFromCVSchema
from src.security import verify_backend_request

load_dotenv()

GENERATE_CV_QUESTION_PROMPT_FILE = os.getenv("GENERATE_CV_QUESTION_PROMPT_FILE", "")
with open(GENERATE_CV_QUESTION_PROMPT_FILE, "r") as prompt_file:
    GENERATE_CV_PROMPT = prompt_file.read()

# gemma_question_generator: Gemma_Question_Generator | None = None

"""@asynccontextmanager
async def lifespan(app: FastAPI):
    # global gemma_question_generator
    # gemma_question_generator = Gemma_Question_Generator(GENERATE_CV_PROMPT)
    global gemma_question_generator
    gemma_question_generator = Gemma_Question_Generator(GENERATE_CV_PROMPT)
    yield"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    global gemma_question_generator
    try:
        gemma_question_generator = Gemma_Question_Generator(GENERATE_CV_PROMPT)
    except Exception as e:
        print(f"⚠️  Gemma non chargé : {e}")
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Hirebox API",
    version="1.0.0",
    docs_url=None,      # Désactive Swagger UI
    redoc_url=None,     # Désactive ReDoc
)

# ─── Scalar UI ────────────────────────────────────────────────────────────────
@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        scalar_proxy_url="https://proxy.scalar.com",  # évite les problèmes CORS
    )

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"message": "Hello Hirebox"}

@app.get("/ping")
async def ping_pong():
    return {"message": "pong", "status": "OK"}


@app.post(
    "/generate-question-from-cv",
    response_model=GenerateQuestionsFromCVDto,
    dependencies=[Depends(verify_backend_request)],
)
async def generate_questions_from_cv(data: GenerateQuestionsFromCVSchema):
    question_generator = Z_AI_Question_Generator(GENERATE_CV_PROMPT)
    handler = GenerateQuestionFromCVHandler(question_generator)
    command = GenerateQuestionFromCVCommandHandler(cv_content=data.cv_content)
    try:
        question_generated = await handler.execute(command)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return GenerateQuestionsFromCVDto(question=question_generated)


# @app.post("/gemma/generate-question-from-cv", response_model=GenerateQuestionsFromCVDto)
# async def gemma_generate_questions_from_cv(data: GenerateQuestionsFromCVSchema):
#     assert gemma_question_generator is not None
#     handler = GenerateQuestionFromCVHandler(gemma_question_generator)
#     command = GenerateQuestionFromCVCommandHandler(
#         cv_content=data.cv_content
#     )
#     try:
#         question_generated = await handler.execute(command)
#     except Exception as e:
#         return HTTPException(status_code=400, detail=str(e))
#     return GenerateQuestionsFromCVDto(question=question_generated)
