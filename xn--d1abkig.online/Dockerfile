FROM python:3.11-slim

# Отключаем запись pyc-файлов и буферизацию вывода Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Версия Poetry
ENV POETRY_VERSION=1.6.1

# Устанавливаем системные зависимости (включая pkg-config и заголовки MySQL)
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

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Копируем только lock-файлы для лучшего кеширования слоёв
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости (только библиотеки, без установки корневого пакета)
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

# Копируем остальной код приложения
COPY . .

# Делаем entrypoint исполняемым
RUN chmod +x /app/entrypoint.sh

# Точка входа
ENTRYPOINT ["/app/entrypoint.sh"]
