FROM python:3.11-slim

# Отключаем запись байткода и буферизацию вывода Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.6.1

# Устанавливаем системные либы для сборки зависимостей
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

# Ставим Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Копируем только pyproject и lock для кеша
COPY pyproject.toml poetry.lock ./

# Генерируем актуальный poetry.lock и ставим зависимости без попытки устанавливать сам пакет
RUN poetry config virtualenvs.create false \
  && poetry lock --no-update \
  && poetry install --no-interaction --no-ansi --no-root

# Копируем весь исходник
COPY . .

# Даём +x entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# В контейнере по умолчанию запустится наш скрипт.
ENTRYPOINT ["/app/entrypoint.sh"]
