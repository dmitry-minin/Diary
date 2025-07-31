FROM python:3.13-slim

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry в систему
RUN poetry config virtualenvs.create false

# Копируем файлы проекта
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry install --no-root

# Копируем остальные файлы
COPY . .

# Устанавливаем права
RUN chmod +x manage.py

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Открываем порт
EXPOSE 8000

# Команда для запуска приложения
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]