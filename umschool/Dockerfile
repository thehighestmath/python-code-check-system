# Базовый образ
FROM python:3.13.7-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/umschool/.local/bin:$PATH"

# Создаем пользователя для безопасности
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Устанавливаем только необходимые системные зависимости
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        curl \
        gcc \
        python3-dev \
        libc6-dev \
        make \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Устанавливаем рабочую директорию
WORKDIR /umschool

# Копируем requirements.txt и устанавливаем зависимости (кэшируемый слой)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# Копируем файлы приложения
COPY . .

# Создаем директории для статических файлов и медиа
RUN mkdir -p /umschool/static /umschool/media /umschool/staticfiles && \
    mkdir -p /umschool/python_code_check_system/static && \
    touch /umschool/static/.gitkeep && \
    rm -rf /umschool/staticfiles/*

# Устанавливаем права доступа ДО переключения пользователя
RUN chmod +x entrypoint.sh entrypoint.test.sh

# Устанавливаем владельца файлов и права доступа
RUN chown -R appuser:appuser /umschool && \
    chmod -R 777 /umschool/static /umschool/media /umschool/staticfiles

# Оставляем root для работы с файлами
# USER appuser

# Открываем порт
EXPOSE 8000

# Команда по умолчанию
CMD ["./entrypoint.sh"]
