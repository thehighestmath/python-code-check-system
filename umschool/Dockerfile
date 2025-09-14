# Многоэтапная сборка для оптимизации
FROM python:3.13.1-slim as builder

# Устанавливаем переменные окружения для сборки
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Устанавливаем системные зависимости для сборки
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
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

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install -r requirements.txt

# Финальный образ
FROM python:3.13.1-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/umschool/.local/bin:$PATH"

# Создаем пользователя для безопасности
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Устанавливаем только runtime зависимости
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        curl \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем установленные пакеты из builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Устанавливаем рабочую директорию
WORKDIR /umschool

# Копируем файлы приложения
COPY . .

# Создаем директории для статических файлов и медиа
RUN mkdir -p /umschool/static /umschool/media

# Устанавливаем права доступа ДО переключения пользователя
RUN chmod +x entrypoint.sh && \
    chown -R appuser:appuser /umschool

# Переключаемся на непривилегированного пользователя
USER appuser

# Открываем порт
EXPOSE 8000

# Команда по умолчанию
CMD ["./entrypoint.sh"]
