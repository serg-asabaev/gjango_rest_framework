FROM python:3.14-slim

# Устанавливаем системные зависимости (нужны для Poetry)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости (без dev-пакетов для production)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

RUN pip install --no-cache-dir "psycopg[binary]"

# Копируем остальной код
COPY . .

# Команда запуска
CMD ["python", "manage.py", "runserver", "8080"]