# Базовый образ
FROM python:3.13.7-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/umschool/.local/bin:$PATH"

# Создаем пользователя для безопасности
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Устанавливаем системные зависимости
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        curl \
        gcc \
        python3-dev \
        libc6-dev \
        linux-libc-dev \
        build-essential \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Устанавливаем рабочую директорию
WORKDIR /umschool

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы приложения
COPY . .

# Создаем директории для статических файлов и медиа
RUN mkdir -p /umschool/static /umschool/media

# Устанавливаем права доступа ДО переключения пользователя
RUN chmod +x entrypoint.sh entrypoint.test.sh

# Устанавливаем владельца файлов
RUN chown -R appuser:appuser /umschool

# Переключаемся на непривилегированного пользователя
USER appuser

# Открываем порт
EXPOSE 8000

# Команда по умолчанию
CMD ["./entrypoint.sh"]
