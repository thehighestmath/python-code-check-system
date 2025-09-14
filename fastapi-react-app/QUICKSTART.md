# Быстрый старт

## 🚀 Запуск приложения

### 1. Клонирование и переход в директорию
```bash
cd fastapi-react-app
```

### 2. Запуск всех сервисов
```bash
./start.sh
```

Или вручную:
```bash
docker-compose up --build
```

### 3. Открытие приложения
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs

## 👤 Тестовые аккаунты

- **Администратор**: `admin` / `admin123`
- **Студент**: `student` / `student123`

## 📋 Что можно делать

1. **Регистрация и вход** - создайте свой аккаунт или войдите как студент
2. **Просмотр заданий** - посмотрите доступные задания разной сложности
3. **Решение заданий** - отправьте свой Python код на проверку
4. **Просмотр результатов** - посмотрите историю своих решений

## 🛠 Разработка

### Backend (FastAPI)
```bash
cd backend
pip install -e .
uvicorn app.main:app --reload
```

### Frontend (React)
```bash
cd frontend
npm install
npm start
```

## 🐳 Docker команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f

# Пересборка
docker-compose up --build
```

## 📁 Структура проекта

```
fastapi-react-app/
├── backend/          # FastAPI backend
├── frontend/         # React frontend  
├── docker-compose.yml
├── start.sh          # Скрипт запуска
└── README.md         # Подробная документация
```

## 🔧 Настройка

Все настройки находятся в файле `backend/.env` (создается автоматически).

## ❓ Проблемы

Если что-то не работает:

1. Проверьте, что Docker запущен
2. Выполните `docker-compose down` и `docker-compose up --build`
3. Проверьте логи: `docker-compose logs`

## 📚 Документация

Полная документация в файле `README.md`.
