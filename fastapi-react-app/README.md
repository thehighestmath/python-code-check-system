# Python Code Check System

Система проверки Python кода с современной архитектурой на FastAPI + React.

## Архитектура

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL + Redis + Celery
- **Frontend**: React + TypeScript + Axios
- **Контейнеризация**: Docker + Docker Compose
- **База данных**: PostgreSQL
- **Кэширование**: Redis
- **Очереди задач**: Celery

## Возможности

- Регистрация и аутентификация пользователей
- Создание и управление заданиями
- Отправка решений на проверку
- Автоматическая проверка Python кода
- Ограничения по времени и памяти
- Проверка на использование запрещенных функций
- История решений пользователя

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Git

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd fastapi-react-app
```

2. Создайте файл `.env` в папке `backend`:
```bash
cp backend/.env.example backend/.env
```

3. Запустите все сервисы:
```bash
docker-compose up --build
```

4. Откройте приложение:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API документация: http://localhost:8000/docs

## Структура проекта

```
fastapi-react-app/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Конфигурация и база данных
│   │   ├── models/         # SQLAlchemy модели
│   │   ├── schemas/        # Pydantic схемы
│   │   └── services/       # Бизнес-логика
│   ├── alembic/            # Миграции базы данных
│   ├── pyproject.toml      # Зависимости Python
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── pages/          # Страницы
│   │   ├── services/       # API сервисы
│   │   └── contexts/       # React контексты
│   ├── package.json        # Зависимости Node.js
│   └── Dockerfile
└── docker-compose.yml      # Конфигурация Docker Compose
```

## API Endpoints

### Аутентификация
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `GET /api/v1/auth/me` - Текущий пользователь

### Задания
- `GET /api/v1/tasks` - Список заданий
- `POST /api/v1/tasks` - Создание задания
- `GET /api/v1/tasks/{id}` - Детали задания
- `PUT /api/v1/tasks/{id}` - Обновление задания
- `DELETE /api/v1/tasks/{id}` - Удаление задания

### Решения
- `GET /api/v1/solutions` - Список решений пользователя
- `POST /api/v1/solutions` - Отправка решения
- `GET /api/v1/solutions/{id}` - Детали решения
- `PUT /api/v1/solutions/{id}` - Обновление решения
- `DELETE /api/v1/solutions/{id}` - Удаление решения

## Разработка

### Backend

1. Установите зависимости:
```bash
cd backend
pip install -e .
```

2. Запустите миграции:
```bash
alembic upgrade head
```

3. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

### Frontend

1. Установите зависимости:
```bash
cd frontend
npm install
```

2. Запустите dev сервер:
```bash
npm start
```

## Тестирование

### Backend тесты
```bash
cd backend
pytest
```

### Frontend тесты
```bash
cd frontend
npm test
```

## Развертывание

1. Настройте переменные окружения в `.env`
2. Соберите и запустите контейнеры:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Лицензия

MIT License
