# Python Code Check System - Makefile
# Удобные команды для разработки и тестирования

.PHONY: help install test test-all test-models test-forms test-views test-core test-docker lint format clean build up down logs shell migrate

# Цвета для вывода
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

help: ## Показать справку по командам
	@echo "$(GREEN)Python Code Check System - Доступные команды:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## Установить зависимости
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	pip install -r umschool/requirements.txt
	pip install coverage pytest black isort flake8 bandit

test: ## Запустить все тесты
	@echo "$(GREEN)Запуск всех тестов...$(NC)"
	cd umschool && python manage.py test --verbosity=2

test-all: ## Запустить все тесты с покрытием
	@echo "$(GREEN)Запуск всех тестов с покрытием...$(NC)"
	cd umschool && coverage run --source='.' manage.py test --verbosity=2
	cd umschool && coverage report --show-missing
	cd umschool && coverage html

test-models: ## Запустить тесты моделей
	@echo "$(GREEN)Запуск тестов моделей...$(NC)"
	cd umschool && python manage.py test python_code_check_system.test_files.test_models --verbosity=2

test-forms: ## Запустить тесты форм
	@echo "$(GREEN)Запуск тестов форм...$(NC)"
	cd umschool && python manage.py test python_code_check_system.test_files.test_forms --verbosity=2

test-views: ## Запустить тесты представлений
	@echo "$(GREEN)Запуск тестов представлений...$(NC)"
	cd umschool && python manage.py test python_code_check_system.test_files.test_views --verbosity=2

test-core: ## Запустить тесты ядра системы
	@echo "$(GREEN)Запуск тестов ядра системы...$(NC)"
	cd umschool && python manage.py test python_code_check_system.check_system.tests --verbosity=2

test-docker: ## Запустить тесты в Docker
	@echo "$(GREEN)Запуск тестов в Docker...$(NC)"
	docker compose up -d
	sleep 10
	docker compose exec server python manage.py test --verbosity=2
	docker compose down

lint: ## Проверить код линтерами
	@echo "$(GREEN)Проверка кода линтерами...$(NC)"
	@echo "$(YELLOW)Running Flake8...$(NC)"
	flake8 $(shell find umschool -name "*.py") || true
	@echo "$(YELLOW)Running Bandit...$(NC)"
	bandit -r umschool/ || true

format: ## Форматировать код
	@echo "$(GREEN)Форматирование кода...$(NC)"
	black $(shell find umschool -name "*.py")
	isort $(shell find umschool -name "*.py")

build: ## Собрать Docker образы
	@echo "$(GREEN)Сборка Docker образов...$(NC)"
	docker compose build --no-cache

up: ## Запустить сервисы
	@echo "$(GREEN)Запуск сервисов...$(NC)"
	docker compose up -d

down: ## Остановить сервисы
	@echo "$(GREEN)Остановка сервисов...$(NC)"
	docker compose down

logs: ## Показать логи сервисов
	@echo "$(GREEN)Логи сервисов:$(NC)"
	docker compose logs -f

shell: ## Войти в контейнер сервера
	@echo "$(GREEN)Вход в контейнер сервера...$(NC)"
	docker compose exec server bash

migrate: ## Применить миграции
	@echo "$(GREEN)Применение миграций...$(NC)"
	cd umschool && python manage.py migrate

migrate-docker: ## Применить миграции в Docker
	@echo "$(GREEN)Применение миграций в Docker...$(NC)"
	docker compose exec server python manage.py migrate

create-superuser: ## Создать суперпользователя
	@echo "$(GREEN)Создание суперпользователя...$(NC)"
	cd umschool && python manage.py createsuperuser

create-superuser-docker: ## Создать суперпользователя в Docker
	@echo "$(GREEN)Создание суперпользователя в Docker...$(NC)"
	docker compose exec server python manage.py createsuperuser

clean: ## Очистить временные файлы
	@echo "$(GREEN)Очистка временных файлов...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf umschool/htmlcov/
	rm -rf umschool/.coverage
	rm -rf umschool/coverage.xml

dev-setup: ## Настройка для разработки
	@echo "$(GREEN)Настройка для разработки...$(NC)"
	cp env.example .env
	make install
	make migrate
	make create-superuser

docker-setup: ## Настройка Docker окружения
	@echo "$(GREEN)Настройка Docker окружения...$(NC)"
	cp env.example .env
	make build
	make up
	sleep 15
	make migrate-docker
	make create-superuser-docker

status: ## Показать статус сервисов
	@echo "$(GREEN)Статус сервисов:$(NC)"
	docker compose ps

restart: ## Перезапустить сервисы
	@echo "$(GREEN)Перезапуск сервисов...$(NC)"
	docker compose restart

backup-db: ## Создать резервную копию БД
	@echo "$(GREEN)Создание резервной копии БД...$(NC)"
	docker compose exec pgdb pg_dump -U postgres python_code_check > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db: ## Восстановить БД из резервной копии
	@echo "$(GREEN)Восстановление БД из резервной копии...$(NC)"
	@echo "$(YELLOW)Использование: make restore-db FILE=backup_file.sql$(NC)"
	docker compose exec -T pgdb psql -U postgres python_code_check < $(FILE)

# Команды для CI/CD
ci-test: ## Команды для CI
	@echo "$(GREEN)Запуск тестов для CI...$(NC)"
	make install
	make test-all
	make lint

ci-docker: ## Команды для CI Docker
	@echo "$(GREEN)Запуск Docker тестов для CI...$(NC)"
	make build
	make up
	sleep 20
	make migrate-docker
	make test-docker
	make down