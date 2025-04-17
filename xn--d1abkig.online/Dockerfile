FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.6.1

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    curl build-essential libpq-dev git \
    && apt-get clean

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Копируем только pyproject и poetry.lock сначала (для кэширования install)
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копируем оставшийся код
COPY . .

# Даём права на запуск entrypoint
RUN chmod +x /app/entrypoint.sh
