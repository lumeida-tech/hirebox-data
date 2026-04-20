# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run dev server (port 8005)
uv run fastapi dev main.py --port 8005

# Type checking
uvx mypy .

# Linting / formatting
uv run ruff check .
uv run ruff format .
```

## Environment Setup

Copy `.env.example` to `.env` and fill in:
- `HF_TOKEN` — Hugging Face API token (used to call GLM-5.1 via `https://router.huggingface.co/v1`)
- `GENERATE_CV_QUESTION_PROMPT_FILE` — path to the prompt text file (e.g. `generate_cv_questions_prompt.txt`)
- `HIREBOX_BACKEND_API_KEY` — API key for authenticating requests to this service

## Architecture

This is a FastAPI service that generates interview questions from CV content using the GLM-5.1 model via HuggingFace's OpenAI-compatible inference router.

**Request flow:**
1. `POST /generate-question-from-cv` in `main.py` receives a `GenerateQuestionsFromCVSchema` (cv_content string)
2. It instantiates `Z_AI_Question_Generator` (in `src/glm_ai.py`) with a system prompt loaded from a file at startup
3. `GenerateQuestionFromCVHandler.execute()` delegates to the generator
4. The generator calls the HuggingFace router using the `openai` SDK with structured output (`response_format=QuestionModel`)
5. Returns a `Question` dataclass serialized as `GenerateQuestionsFromCVDto`

**Key abstractions:**
- `src/spi.py` — `QuestionGenerator` Protocol (the interface all AI backends must implement)
- `src/question.py` — `Question` dataclass (the domain model)
- `src/glm_ai.py` — `Z_AI_Question_Generator` (concrete implementation using GLM-5.1 via HuggingFace)
- `src/generate_question_handler.py` — command/handler pattern wrapping the generator
- `src/api.py` — Pydantic schemas for HTTP request/response

The model used is `"zai-org/GLM-5.1:together"` accessed through `https://router.huggingface.co/v1` with the OpenAI client.
