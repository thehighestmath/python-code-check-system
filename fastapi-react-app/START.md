# 🚀 Запуск проекта FastAPI + React

## ✅ Проект успешно запущен!

### 🌐 Доступные сервисы:

- **Frontend (React)**: http://localhost:3000
- **Backend API (FastAPI)**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

### 👤 Тестовые аккаунты:

- **Администратор**: `admin` / `admin123`
- **Студент**: `student` / `student123`

## 🛠 Управление сервисами

### Запуск всех сервисов:
```bash
# 1. Запустить базу данных
./start-db.sh

# 2. Запустить backend (в одном терминале)
./start-backend.sh

# 3. Запустить frontend (в другом терминале)
./start-frontend.sh
```

### Остановка сервисов:
```bash
# Остановить базу данных
docker-compose -f docker-compose.dev.yml down

# Остановить backend и frontend
# Нажать Ctrl+C в соответствующих терминалах
```

## 📋 Что можно делать:

1. **Регистрация и вход** - создайте свой аккаунт или войдите как студент
2. **Просмотр заданий** - посмотрите доступные задания разной сложности
3. **Решение заданий** - отправьте свой Python код на проверку
4. **Просмотр результатов** - посмотрите историю своих решений

## 🔧 Разработка

### Backend (FastAPI):
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend (React):
```bash
cd frontend
npm start
```

### База данных:
```bash
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

## 📁 Структура проекта:

```
fastapi-react-app/
├── backend/                 # FastAPI backend
│   ├── app/                # Основной код
│   ├── venv/               # Python окружение
│   └── .env                # Настройки
├── frontend/               # React frontend
│   ├── src/                # Исходный код
│   └── .env                # Настройки
└── docker-compose.dev.yml  # База данных
```

## 🎉 Готово к работе!

Проект полностью настроен и готов к разработке. Все сервисы запущены и работают корректно.
