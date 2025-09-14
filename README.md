# Python Code Check System

Система для проверки Python кода с автоматическим тестированием на Django.

## 🚀 Быстрый старт

### Требования
- Docker и Docker Compose
- Make (опционально, для удобства)

### Установка

1. **Клонируйте репозиторий**
   ```bash
   git clone <repository-url>
   cd python-code-check-system
   ```

2. **Настройте окружение**
   ```bash
   cp env.example .env
   # При необходимости отредактируйте .env
   ```

3. **Запустите систему**
   ```bash
   # Используя Make (рекомендуется)
   make up-build
   
   # Или напрямую через Docker Compose
   docker-compose up --build -d
   ```

4. **Откройте приложение**
   - Веб-интерфейс: http://localhost:80
   - Админ-панель: http://localhost:80/admin
   - Логин: admin, Пароль: admin

## 📋 Доступные команды

```bash
# Показать все команды
make help

# Запустить все сервисы
make up

# Остановить все сервисы
make down

# Просмотр логов
make logs

# Просмотр логов в реальном времени
make logs-f

# Запустить тесты
make test

# Войти в контейнер сервера
make shell

# Очистить все
make clean
```

## 👥 Тестовые аккаунты

Система автоматически создает тестовые аккаунты:
- **Студент**: student1 / student123
- **Учитель**: teacher1 / teacher123
- **Админ**: admin / admin

## 🏗️ Архитектура

- **Backend**: Django 5.0.9
- **База данных**: PostgreSQL 16.3
- **Кэш/Очередь**: Redis 7.0.15
- **Очередь задач**: Celery 5.3.6
- **Контейнеризация**: Docker & Docker Compose

## 🔧 Разработка

Для разработки с hot reload:

```bash
# Запустить только сервер с монтированием volumes
make dev

# Или запустить локально с виртуальным окружением
cd umschool
source ../venv/bin/activate
python manage.py runserver
```

## 🐛 Устранение неполадок

### Частые проблемы

1. **Ошибки подключения к БД**
   - Убедитесь, что PostgreSQL запущен
   - Проверьте учетные данные в `.env`

2. **Ошибки прав доступа**
   - Выполните `make clean` и попробуйте снова
   - Проверьте права Docker

3. **Конфликты портов**
   - Измените маппинг портов в `docker-compose.yaml`
   - Или остановите конфликтующие сервисы

### Логи

```bash
# Просмотр всех логов
make logs

# Просмотр логов конкретного сервиса
docker-compose logs server
docker-compose logs pgdb
docker-compose logs redis
```

## 📝 Важные замечания

> [!IMPORTANT]
> - Убедитесь, что концы строк установлены как LF, а не CRLF
> - Создайте файл `.env` в корне репозитория на основе `env.example`
> - Для Windows: https://docs.docker.com/desktop/install/windows-install/
> - Для Linux: https://docs.docker.com/engine/install/ubuntu/
> - Для macOS: https://docs.docker.com/desktop/install/mac-install/

## 🌐 Тестовое окружение

Развернутое тестовое окружение доступно по адресу: http://158.160.28.235/
