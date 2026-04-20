FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH" \
    HOME=/home/app \
    HF_HOME=/home/app/.cache/huggingface

WORKDIR /app

RUN groupadd --system hirebox \
    && useradd --system --gid hirebox --create-home --home-dir /home/hirebox hirebox

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY --chown=hirebox:hirebox main.py ./
COPY --chown=hirebox:hirebox moussa_generate_cv_questions_prompt.md ./generate_cv_questions_prompt.txt
COPY --chown=hirebox:hirebox src ./src

USER hirebox

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]