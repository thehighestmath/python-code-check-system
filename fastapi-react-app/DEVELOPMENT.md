# Локальная разработка

## Предварительные требования

### 1. Python 3.11+
```bash
# Проверить версию
python3 --version

# Если не установлен, установить через Homebrew (macOS)
brew install python@3.11
```

### 2. Node.js 18+
```bash
# Установить через Homebrew (macOS)
brew install node

# Или через nvm (рекомендуется)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### 3. PostgreSQL (опционально - можно использовать Docker)
```bash
# Установить через Homebrew (macOS)
brew install postgresql
brew services start postgresql

# Или использовать Docker (рекомендуется)
```

### 4. Redis (опционально - можно использовать Docker)
```bash
# Установить через Homebrew (macOS)
brew install redis
brew services start redis

# Или использовать Docker (рекомендуется)
```

## Быстрая настройка

1. **Установите зависимости:**
   ```bash
   ./setup-dev.sh
   ```

2. **Запустите базу данных:**
   ```bash
   ./start-db.sh
   ```

3. **Инициализируйте базу данных:**
   ```bash
   cd backend
   source venv/bin/activate
   python init_db.py
   ```

4. **Запустите backend (в одном терминале):**
   ```bash
   ./start-backend.sh
   ```

5. **Запустите frontend (в другом терминале):**
   ```bash
   ./start-frontend.sh
   ```

## Доступ к приложению

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs

## Тестовые аккаунты

- **Администратор**: `admin` / `admin123`
- **Студент**: `student` / `student123`

## Полезные команды

### Backend
```bash
cd backend
source venv/bin/activate

# Запуск сервера
uvicorn app.main:app --reload

# Миграции
alembic upgrade head
alembic revision --autogenerate -m "Description"

# Тесты
pytest

# Инициализация БД
python init_db.py
```

### Frontend
```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev сервера
npm start

# Сборка для продакшена
npm run build

# Тесты
npm test
```

### База данных
```bash
# Запуск через Docker
docker-compose -f docker-compose.dev.yml up -d

# Остановка
docker-compose -f docker-compose.dev.yml down

# Подключение к PostgreSQL
psql -h localhost -U postgres -d python_code_check
```

## Структура проекта

```
fastapi-react-app/
├── backend/                 # FastAPI backend
│   ├── app/                # Основной код приложения
│   ├── alembic/            # Миграции БД
│   ├── venv/               # Python виртуальное окружение
│   ├── .env                # Переменные окружения
│   └── pyproject.toml      # Зависимости Python
├── frontend/               # React frontend
│   ├── src/                # Исходный код
│   ├── node_modules/       # Node.js зависимости
│   └── .env                # Переменные окружения
├── docker-compose.dev.yml  # Docker для БД
└── *.sh                    # Скрипты для разработки
```

## Отладка

### Backend не запускается
1. Проверьте, что виртуальное окружение активировано
2. Проверьте, что все зависимости установлены: `pip list`
3. Проверьте, что база данных запущена
4. Проверьте логи: `uvicorn app.main:app --reload --log-level debug`

### Frontend не запускается
1. Проверьте, что Node.js установлен: `node --version`
2. Проверьте, что зависимости установлены: `npm list`
3. Очистите кэш: `npm start -- --reset-cache`

### База данных недоступна
1. Проверьте, что PostgreSQL запущен: `brew services list | grep postgres`
2. Проверьте подключение: `psql -h localhost -U postgres`
3. Используйте Docker: `./start-db.sh`
