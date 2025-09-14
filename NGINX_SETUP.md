# 🌐 Настройка Nginx для Python Code Check System

## 📋 Обзор

Nginx будет работать как reverse proxy для Django приложения, обеспечивая:
- Статическую раздачу файлов
- Балансировку нагрузки
- SSL терминацию
- Кэширование
- Безопасность

## 🚀 Быстрая настройка

### 1. Подготовка файлов

```bash
# На сервере скопируйте файлы:
scp nginx.conf setup-nginx.sh root@158.160.28.235:/root/
```

### 2. Запуск автоматической настройки

```bash
# На сервере выполните:
sudo bash setup-nginx.sh
```

## 🔧 Ручная настройка

### 1. Установка Nginx

```bash
sudo apt update
sudo apt install -y nginx
```

### 2. Создание конфигурации

```bash
# Копируем конфигурацию
sudo cp nginx.conf /etc/nginx/sites-available/python-code-check-system

# Активируем сайт
sudo ln -s /etc/nginx/sites-available/python-code-check-system /etc/nginx/sites-enabled/

# Удаляем дефолтный сайт
sudo rm -f /etc/nginx/sites-enabled/default
```

### 3. Проверка и запуск

```bash
# Проверяем конфигурацию
sudo nginx -t

# Перезапускаем Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## 🔒 Настройка SSL (опционально)

### 1. Установка Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 2. Получение сертификата

```bash
# Замените example.com на ваш домен
sudo certbot --nginx -d example.com
```

### 3. Автоматическое обновление

```bash
sudo crontab -e
# Добавьте строку:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Мониторинг

### Просмотр логов

```bash
# Логи доступа
tail -f /var/log/nginx/python-code-check-system.access.log

# Логи ошибок
tail -f /var/log/nginx/python-code-check-system.error.log

# Все логи Nginx
journalctl -u nginx -f
```

### Проверка статуса

```bash
# Статус Nginx
systemctl status nginx

# Проверка конфигурации
nginx -t

# Перезапуск
systemctl restart nginx
```

## 🛡️ Безопасность

### Firewall настройки

```bash
# Разрешаем HTTP и HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

### Дополнительные настройки безопасности

В файле `/etc/nginx/sites-available/python-code-check-system` уже включены:
- Заголовки безопасности
- Ограничение скорости запросов
- Блокировка подозрительных запросов
- Скрытие версии Nginx

## 🔧 Настройка Django для работы с Nginx

### 1. Обновите ALLOWED_HOSTS

В вашем `.env` файле на сервере:

```bash
# Добавьте домен или IP в ALLOWED_HOSTS
echo "ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,yourdomain.com" >> .env
```

### 2. Соберите статические файлы

```bash
# В Docker контейнере
docker compose exec server python manage.py collectstatic --noinput
```

### 3. Перезапустите Django

```bash
docker compose restart server
```

## 🌐 Проверка работы

После настройки проверьте:

1. **HTTP доступ**: http://158.160.28.235:8000
2. **Статические файлы**: http://158.160.28.235:8000/static/
3. **Логи Nginx**: `tail -f /var/log/nginx/python-code-check-system.access.log`

## 🚨 Устранение проблем

### Ошибка 502 Bad Gateway

```bash
# Проверьте, что Django запущен на порту 8000
docker compose ps
netstat -tlnp | grep :8000
```

### Ошибка 404 для статических файлов

```bash
# Проверьте права доступа к статическим файлам
ls -la /umschool/static/
sudo chown -R www-data:www-data /umschool/static/
```

### Nginx не запускается

```bash
# Проверьте конфигурацию
nginx -t

# Просмотрите логи
journalctl -u nginx -n 50
```

## 📈 Оптимизация производительности

### 1. Настройка кэширования

Добавьте в конфигурацию Nginx:

```nginx
# Кэширование для статических файлов
location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 2. Сжатие

```nginx
# В блоке server добавьте:
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

## 🎯 Результат

После настройки у вас будет:
- ✅ Nginx как reverse proxy
- ✅ Статическая раздача файлов
- ✅ SSL поддержка (если настроено)
- ✅ Безопасность и производительность
- ✅ Логирование и мониторинг

Ваш сайт будет доступен по адресу: **http://158.160.28.235:8000** 🚀
