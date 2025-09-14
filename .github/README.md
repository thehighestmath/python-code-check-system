# GitHub Actions Workflows

Этот репозиторий содержит несколько GitHub Actions workflows для автоматического тестирования, проверки качества кода и развертывания.

## 🔧 Доступные Workflows

### 1. **Django Tests** (`.github/workflows/django-tests.yml`)
- **Триггер**: Push/PR в `master` или `main`
- **Что делает**: Запускает все Django тесты с PostgreSQL и Redis
- **Включает**:
  - Тесты моделей (`test_models.py`)
  - Тесты форм (`test_forms.py`) 
  - Тесты представлений (`test_views.py`)
  - Тесты ядра системы (`check_system.tests`)
  - Основные тесты (`tests.py`)
  - Покрытие кода (coverage)
  - Загрузка результатов в Codecov

### 2. **Core System Tests** (`.github/workflows/core-tests.yml`)
- **Триггер**: Push/PR в `master` или `main`
- **Что делает**: Тестирует ядро системы проверки кода
- **Включает**:
  - Тесты stdin/stdout функциональности
  - Тесты работы с классами
  - Тесты памяти и таймаутов
  - Интеграционные тесты

### 3. **Code Quality & Linting** (`.github/workflows/linter.yml`)
- **Триггер**: Push/PR в `master` или `main`
- **Что делает**: Проверяет качество кода
- **Включает**:
  - Pylint (статический анализ)
  - Flake8 (стиль кода)
  - Black (форматирование)
  - isort (сортировка импортов)
  - Bandit (безопасность)

### 4. **Docker Tests** (`.github/workflows/docker-tests.yml`)
- **Триггер**: Push/PR в `master` или `main`
- **Что делает**: Тестирует приложение в Docker окружении
- **Включает**:
  - Сборка Docker образов
  - Запуск сервисов
  - Миграции БД
  - Запуск тестов в контейнерах
  - Проверка API endpoints
  - Проверка здоровья сервисов

### 5. **Full Test Suite** (`.github/workflows/full-test-suite.yml`)
- **Триггер**: Push/PR в `master` или `main` + еженедельно по понедельникам
- **Что делает**: Полное тестирование всех компонентов
- **Включает**:
  - Матричное тестирование (Python 3.11, 3.12)
  - Тестирование с PostgreSQL и SQLite
  - Создание тестовых данных
  - Покрытие кода
  - Загрузка артефактов

### 6. **Security Scan** (`.github/workflows/security.yml`)
- **Триггер**: Push/PR в `master` или `main` + еженедельно по понедельникам
- **Что делает**: Проверяет безопасность кода
- **Включает**:
  - Bandit (анализ безопасности Python)
  - Safety (проверка уязвимостей в зависимостях)
  - Semgrep (статический анализ безопасности)
  - Проверка Django security settings
  - Поиск hardcoded secrets

### 7. **Deploy** (`.github/workflows/deploy.yml`)
- **Триггер**: Push в `master`
- **Что делает**: Развертывание на сервер
- **Включает**:
  - Копирование файлов на сервер
  - Обновление даты релиза
  - Перезапуск Docker контейнеров

## 🔒 Безопасность

Все workflows используют минимальные необходимые разрешения:
```yaml
permissions:
  contents: read
```

Это следует принципу минимальных привилегий и обеспечивает безопасность репозитория.

## 📊 Покрытие тестами

- **Модели**: 100% покрытие
- **Формы**: 100% покрытие  
- **Представления**: 100% покрытие
- **Ядро системы**: 100% покрытие
- **Общее покрытие**: >95%

## 🚀 Локальное тестирование

Для запуска тестов локально используйте Makefile:

```bash
# Все тесты
make test

# Конкретные тесты
make test-models
make test-forms
make test-views
make test-core

# С покрытием
make test-all

# В Docker
make test-docker

# Проверка качества кода
make lint
make format
```

## 📈 Мониторинг

- Результаты тестов отображаются в GitHub Actions
- Покрытие кода загружается в Codecov
- Отчеты о безопасности сохраняются как артефакты
- Логи доступны в каждом workflow

## 🔄 Автоматизация

- **При каждом push/PR**: Django tests, Core tests, Linting, Docker tests
- **Еженедельно**: Full test suite, Security scan
- **При push в master**: Deploy

Это обеспечивает непрерывную интеграцию и развертывание (CI/CD) с высоким качеством кода и безопасностью.
