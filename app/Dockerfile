FROM python:3.13-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=2.1.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    build-essential \
    gcc \
    python3-dev &&\
    pip install --no-cache-dir \
    "poetry==$POETRY_VERSION" && \
    apt-get remove --purge -y build-essential python3-dev && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    poetry --version

WORKDIR /app

# Копируем ТОЛЬКО файлы зависимостей
COPY ./app/pyproject.toml ./app/poetry.lock* ./

# Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем весь остальной код
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]