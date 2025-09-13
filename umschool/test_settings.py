"""
Настройки для тестирования
Отдельный файл настроек для запуска тестов без Redis и с SQLite
"""

from umschool.settings import *  # noqa: F403

# Переопределяем настройки для тестирования
DEBUG = True

# Используем SQLite для тестов (быстрее)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Отключаем кеширование для тестов
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Используем файловую систему для сессий
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Отключаем Celery для тестов
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Отключаем логирование для тестов
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
    },
}


# Отключаем миграции для тестов (используем --nomigrations)
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Настройки безопасности для тестов
SECRET_KEY = 'test-secret-key-for-testing-only'
ALLOWED_HOSTS = ['*']

# Отключаем валидацию паролей для тестов
AUTH_PASSWORD_VALIDATORS = []

# Настройки для тестирования
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Отключаем CSRF для тестов
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = None

# Настройки для тестирования файлов
MEDIA_ROOT = '/tmp/test_media/'
STATIC_ROOT = '/tmp/test_static/'

# Отключаем email для тестов
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Настройки для тестирования Celery
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

# Настройки для тестирования Redis
REDIS_URI = 'redis://localhost:6379/1'

# Отключаем HSTS для тестов
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Настройки для тестирования
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
