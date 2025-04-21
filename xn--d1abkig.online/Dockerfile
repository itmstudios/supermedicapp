FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.6.1

# Install system dependencies (including pkg-config and MySQL client headers)
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

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Copy only lock files first for better layer caching
COPY pyproject.toml poetry.lock ./

# Install python dependencies system‑wide
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy the rest of your application code
COPY . .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# let docker-compose handle the final up
