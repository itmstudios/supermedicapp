FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.6.1

# Системные библиотеки для сборки mysqlclient/psycopg2
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    python3-dev \
    libpq-dev \
    git \
    pkg-config \
    default-libmysqlclient-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Кешируем зависимос­ти
COPY pyproject.toml poetry.lock ./

# Обновляем lock-файл и ставим всё (без попытки установить сам пакет)
RUN poetry config virtualenvs.create false \
  && poetry lock --no-update \
  && poetry install --no-interaction --no-ansi --no-root

# Копируем приложение
COPY . .

# Гарантируем +x
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
