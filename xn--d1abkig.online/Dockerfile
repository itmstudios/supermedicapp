FROM python:3.11-slim

# Отключаем запись байткодов и буферизацию вывода Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.6.1

# Устанавливаем системные зависимости
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

# Копируем pyproject.toml и poetry.lock для кеширования слоёв
COPY pyproject.toml poetry.lock ./

# Устанавливаем все зависимости из lock-файла, без попытки установить сам проект
# Затем дополняем окружение gunicorn'ом через pip, обойдя несовместимость lock-файла
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root \
  && pip install --no-cache-dir gunicorn==20.1.0

# Копируем весь код приложения
COPY . .

# Даем права на исполнение entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Точка входа — переопределяется в docker-compose, но пусть будет запасная
ENTRYPOINT ["/app/entrypoint.sh"]
